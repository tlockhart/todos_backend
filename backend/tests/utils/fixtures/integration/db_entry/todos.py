import pytest
from ....factories.auth import TodosFactory


@pytest.fixture
def todo_db_entry(object_db_entry, user_with_todos_db_entry):
    """
    SINGLE RESOURCE PROVISIONER:
    Creates exactly one Todo for the user provided by 'user_with_todos_db_entry'.
    - Primary Use: Tests for specific resource endpoints (e.g., GET /todos/todo/{id}).
    - This ensures the resource being tested is owned by the logged-in user.
    """
    return object_db_entry(
        TodosFactory,
        owner=user_with_todos_db_entry,
        owner_id=user_with_todos_db_entry.id,
    )
