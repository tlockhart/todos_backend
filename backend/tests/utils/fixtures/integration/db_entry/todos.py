import pytest
from ....factories.todos import TodosFactory


@pytest.fixture
def todo_db_entry(object_db_entry):
    """
    SINGLE RESOURCE PROVISIONER:
    Creates exactly one Todo.
    - Primary Use: Tests for specific resource endpoints (e.g., GET /todos/todo/{id}).
    - Returns a function so you can override fields (title, owner, etc.).
    """

    # DJANGO SUBSTITUTION:
    # return lambda **kwargs: TodosFactory.create(**kwargs)
    def _create_todo(**kwargs):
        return object_db_entry(TodosFactory, **kwargs)

    return _create_todo
