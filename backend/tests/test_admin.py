from .utils import *
from fastapi import status
from fastapi.testclient import TestClient
import pytest
from ..main import app
from ..models import Todos
from ..utils.database.connection import get_current_user
from .utils.test_db_setup import override_get_current_user
from .utils.factories.auth import UserFactory

client = TestClient(app)


def test_admin_read_all_authenticated(test_todo):
    # Manually override for this specific test (Happy Path)
    app.dependency_overrides[get_current_user] = override_get_current_user

    response = client.get("/admin/todo")
    assert response.status_code == 200
    assert response.json() == [
        {
            "complete": test_todo.complete,
            "title": test_todo.title,
            "description": test_todo.description,
            "priority": test_todo.priority,
            "owner_id": test_todo.owner_id,
            "id": test_todo.id,
        }
    ]
    # Cleanup
    del app.dependency_overrides[get_current_user]


def test_admin_delete_todo(test_todo, test_db_session):
    app.dependency_overrides[get_current_user] = override_get_current_user

    response = client.delete("/admin/todo/1")
    assert response.status_code == 200

    model = test_db_session.query(Todos).filter(Todos.id == 1).first()
    assert model is None
    del app.dependency_overrides[get_current_user]


def test_admin_delete_todo_not_found(test_todo):
    app.dependency_overrides[get_current_user] = override_get_current_user

    response = client.delete("/admin/todo/999")
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
