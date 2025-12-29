from fastapi import status
from fastapi.testclient import TestClient
import pytest
from ...main import app
from ...models import Todos
from ...utils.database.connection import get_current_user
from ..utils.test_db_setup import override_get_current_user, test_todo, test_db_session
from ..utils.factories.auth import UserFactory

client = TestClient(app)

# ------------------------------------------------------------------------------
# LOCAL DEPENDENCY OVERRIDES (Scenario-Specific)
# ------------------------------------------------------------------------------
# Unlike the GLOBAL overrides in conftest.py (which handle infrastructure like DB),
# these LOCAL overrides handle "Business Logic" scenarios.
# We override 'get_current_user' per-test to simulate specific user roles (Admin)
# or identities, ensuring we test permissions correctly without affecting other tests.
#
# Why pass 'test_todo' and 'test_db_session' as arguments?
# While dependency_overrides handle the *Application's* access to the DB/User,
# we pass these fixtures to the *Test Function* to allow for:
# 1. Arrange: Seeding data (test_todo) before the request.
# 2. Assert: Verifying database state (test_db_session) after the request.
# ------------------------------------------------------------------------------


def test_admin_read_all_authenticated(test_todo):
    # Manually override for this specific test (Happy Path)
    # DJANGO SUBSTITUTION: Use client.force_login(user) instead of dependency overrides.
    app.dependency_overrides[get_current_user] = override_get_current_user

    response = client.get("/admin/todo")
    assert response.status_code == 200
    data = response.json()
    # Robust assertion: Find the specific todo by ID in the list
    found_todo = next((item for item in data if item["id"] == test_todo.id), None)
    assert found_todo is not None, f"Todo with id {test_todo.id} not found in response"
    assert found_todo["title"] == test_todo.title
    assert found_todo["description"] == test_todo.description
    assert found_todo["priority"] == test_todo.priority
    assert found_todo["complete"] == test_todo.complete
    assert found_todo["owner_id"] == test_todo.owner_id

    # Cleanup
    del app.dependency_overrides[get_current_user]


def test_admin_delete_todo(test_todo, test_db_session):
    # DJANGO SUBSTITUTION: Use client.force_login(user) instead of dependency overrides.
    app.dependency_overrides[get_current_user] = override_get_current_user

    response = client.delete(f"/admin/todo/{test_todo.id}")
    assert response.status_code == 200

    # DJANGO SUBSTITUTION: Use Todos.objects.filter(id=test_todo.id).first()
    model = test_db_session.query(Todos).filter(Todos.id == test_todo.id).first()
    assert model is None
    del app.dependency_overrides[get_current_user]


def test_admin_delete_todo_not_found(test_todo):
    # DJANGO SUBSTITUTION: Use client.force_login(user) instead of dependency overrides.
    app.dependency_overrides[get_current_user] = override_get_current_user

    response = client.delete(f"/admin/todo/{test_todo.id + 999}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found."}
    del app.dependency_overrides[get_current_user]


# ------------------------------------------------------------------------------
# PARAMETERIZED INTEGRATION TEST
# ------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "role, expected_status",
    [
        ("admin", 200),  # Should succeed
        ("user", 401),  # Should fail (Access Denied / Unauthorized)
    ],
)
def test_admin_route_permissions(role, expected_status):
    # 1. Create a user with the specific role using your Factory
    # We use .build() because we don't need it in the DB, just for the token payload
    user = UserFactory.build(role=role, id=1)

    # 2. Override the dependency to return THIS specific user
    # DJANGO SUBSTITUTION: Use client.force_login(user) instead of dependency overrides.
    app.dependency_overrides[get_current_user] = lambda: {
        "username": user.username,
        "id": user.id,
        "user_role": user.role,
    }

    # 3. Run the test
    response = client.get("/admin/todo")
    assert response.status_code == expected_status

    # 4. Cleanup
    del app.dependency_overrides[get_current_user]
