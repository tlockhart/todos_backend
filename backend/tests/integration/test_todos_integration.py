from fastapi.testclient import TestClient
from starlette import status
from backend.main import app
from backend.models import Todos

client = TestClient(app)

# -------------------------------------------------
# INTEGRATION TEST
# -------------------------------------------------
def test_read_all_todos(user_with_todos):
    """
    INTEGRATION:
    - user_with_todos creates 3 todos
    - API returns all of them
    """

    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert len(data) == 3

    owner_ids = {todo["owner_id"] for todo in data}
    assert owner_ids == {user_with_todos.id}


# -------------------------------------------------
# INTEGRATION TEST
# -------------------------------------------------
def test_read_single_todo(todo):
    response = client.get(f"/todos/todo/{todo.id}")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["title"] == todo.title


# -------------------------------------------------
# INTEGRATION TEST
# -------------------------------------------------
def test_update_todo(todo, db):
    payload = {
        "title": "Updated",
        "description": "Updated",
        "priority": 1,
        "complete": True,
    }

    response = client.put(f"/todos/todo/{todo.id}", json=payload)
    assert response.status_code == 200

    db.refresh(todo)
    assert todo.complete is True


# -------------------------------------------------
# INTEGRATION TEST
# -------------------------------------------------
def test_delete_todo(todo, db):
    response = client.delete(f"/todos/todo/{todo.id}")
    assert response.status_code == 200

    assert db.get(Todos, todo.id) is None