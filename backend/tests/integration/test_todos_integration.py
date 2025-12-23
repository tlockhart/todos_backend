from fastapi.testclient import TestClient
from starlette import status
from ...main import app
from ...models import Todos

client = TestClient(app)

# -------------------------------------------------
# INTEGRATION TEST
# -------------------------------------------------
def test_read_all_todos(client_with_user, user_with_todos_db_entry):
    response = client_with_user.get("/todos")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 3
    owner_ids = {todo["owner_id"] for todo in data}
    # NOTE: Rule #1: Never assert fixed IDs
    # assert owner_ids == {1}  # or user_with_todos_db_entry.id
    assert owner_ids == {user_with_todos_db_entry.id}


# -------------------------------------------------
# INTEGRATION TEST
# -------------------------------------------------
def test_read_single_todo(client_with_user, todo_db_entry):
    response = client_with_user.get(f"/todos/todo/{todo_db_entry.id}")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["title"] == todo_db_entry.title


# -------------------------------------------------
# INTEGRATION TEST
# -------------------------------------------------
def test_update_todo(client_with_user, todo_db_entry, test_db_session):
    payload = {
        "title": "Updated",
        "description": "Updated",
        "priority": 1,
        "complete": True,
    }

    response = client_with_user.put(f"/todos/todo/{todo_db_entry.id}", json=payload)
    assert response.status_code == 200

     # Reload the todo from the database in a fresh session
    updated_todo = test_db_session.get(Todos, todo_db_entry.id)
    test_db_session.refresh(updated_todo)
    assert updated_todo.complete is True
    assert updated_todo.title == "Updated"


# -------------------------------------------------
# INTEGRATION TEST
# -------------------------------------------------
def test_delete_todo(client_with_user, todo_db_entry, test_db_session):
    response = client_with_user.delete(f"/todos/todo/{todo_db_entry.id}")
    assert response.status_code == 200
    
    """Instead of test_db_session.refresh(todo_db_entry), query fresh
    Even though you expect the row to be gone, SQLAlchemy 
    still has the object in the session as a pending delete, 
    so calling test_db_session.get() or test_db_session.refresh() on it will fail."""
    # deleted_todo = test_db_session.get(Todos, todo_db_entry.id)
    
    # Solution: Query the test_db_session with will not pull object in pending state:
    deleted_todo = test_db_session.query(Todos).filter(Todos.id == todo_db_entry.id).first()
    
    assert deleted_todo is None