from fastapi.testclient import TestClient
from starlette import status
from ...main import app
from ...models import Todos

client = TestClient(app)

# -------------------------------------------------
# INTEGRATION TEST
# -------------------------------------------------
def test_read_all_todos(user_with_todos_db_entry):
    """
    INTEGRATION:
    - user_with_todos_db_entry creates 3 todos
    - API returns all of them
    """

    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert len(data) == 3

    owner_ids = {todo["owner_id"] for todo in data}
    assert owner_ids == {user_with_todos_db_entry.id}


# -------------------------------------------------
# INTEGRATION TEST
# -------------------------------------------------
def test_read_single_todo(todo_db_entry):
    response = client.get(f"/todos/todo/{todo_db_entry.id}")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["title"] == todo_db_entry.title


# -------------------------------------------------
# INTEGRATION TEST
# -------------------------------------------------
def test_update_todo(todo_db_entry, db):
    payload = {
        "title": "Updated",
        "description": "Updated",
        "priority": 1,
        "complete": True,
    }

    response = client.put(f"/todos/todo/{todo_db_entry.id}", json=payload)
    assert response.status_code == 200

    db.refresh(todo_db_entry)
    assert todo_db_entry.complete is True


# -------------------------------------------------
# INTEGRATION TEST
# -------------------------------------------------
def test_delete_todo(todo_db_entry, db):
    response = client.delete(f"/todos/todo/{todo_db_entry.id}")
    assert response.status_code == 200

    assert db.get(Todos, todo_db_entry.id) is None