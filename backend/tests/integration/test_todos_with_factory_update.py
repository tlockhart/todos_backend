from starlette import status
from ...utils.database.connection import get_current_user
from ..utils.db_connections import (
    TestingSessionLocal,
    override_get_current_user,
    test_todo,
)
from ...models import Todos
from fastapi.testclient import TestClient
from ...main import app
import pytest

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_overrides():
    # get_db_session is already overridden globally in conftest.py
    # We only need to override the user for these authenticated tests
    app.dependency_overrides[get_current_user] = override_get_current_user
    yield
    del app.dependency_overrides[get_current_user]


# Pass the test_todo into the test
def test_read_all_authenticated(test_todo):
    # ensure the fixture created a todo and the endpoint returns it
    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    # Make assertions about the returned todo fields (ignore auto-generated id)
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    item = data[0]
    assert item["title"] == test_todo.title
    assert item["description"] == test_todo.description
    assert item["priority"] == test_todo.priority
    assert item["complete"] == test_todo.complete
    assert item["owner_id"] == test_todo.owner_id

    # --- also assert the returned JSON equals the fixture's serialized model ---
    from sqlalchemy import inspect

    def model_to_dict(obj):
        # convert SQLAlchemy ORM instance to a dict of column values
        return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

    expected = model_to_dict(test_todo)
    assert item == expected


def test_read_one_authenticated(test_todo):
    # ensure the fixture created a todo and the endpoint returns it
    response = client.get("/todos/todo/1")
    assert response.status_code == status.HTTP_200_OK
    # Make assertions about the returned todo fields (ignore auto-generated id)
    data = response.json()
    # assert isinstance(data, dict)

    assert data["title"] == test_todo.title
    assert data["description"] == test_todo.description
    assert data["priority"] == test_todo.priority
    assert data["complete"] == test_todo.complete
    assert data["owner_id"] == test_todo.owner_id


def test_read_one_authenticated_not_found():
    response = client.get("/todos/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["detail"] == "Todo not found."


def test_create_todo(test_todo):
    request_data = {
        "title": "New Todo!",
        "description": "New todo description",
        "priority": 5,
        "complete": False,
    }
    # pass in a new json as ToDoRequest
    response = client.post("/todos/todo", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    # check if data stored:
    db = TestingSessionLocal()
    model = db.get(Todos, 2)
    assert model is not None
    assert model.title == request_data.get("title")
    assert model.description == request_data.get("description")
    assert model.priority == request_data.get("priority")
    assert model.complete == request_data.get("complete")


def test_update_todo(test_todo):
    request_data = {
        "title": "Change the title of the todo already saved!",
        "description": "Need to learn everday!",
        "priority": 5,
        "complete": False,
    }
    response = client.put("/todos/todo/1", json=request_data)
    assert response.status_code == 200
    # Validate data in db
    db = TestingSessionLocal()
    model = db.get(Todos, 1)
    assert model.title == "Change the title of the todo already saved!"


def test_update_todo_not_found(test_todo):
    request_data = {
        "title": "Change the title of the todo already saved!",
        "description": "Need to learn everday!",
        "priority": 5,
        "complete": False,
    }

    response = client.put("/todos/todo/999", json=request_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found."


def test_delete_todo(test_todo):
    response = client.delete("/todos/todo/1")
    assert response.status_code == 200
    db = TestingSessionLocal()
    model = db.get(Todos, 1)
    assert model is None


def test_delete_todo_not_found(test_todo):
    response = client.delete("/todos/todo/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found."
