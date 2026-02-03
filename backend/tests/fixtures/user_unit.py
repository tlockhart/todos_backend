import pytest
from typing import Callable
from ..factories.auth import UserFactory
from ..factories.todos import TodosFactory


# -------------------------------------------------
# UNIT TEST fixtures - no database interaction
# -------------------------------------------------
@pytest.fixture
def user():
    """Create a user instance (not persisted to database)."""
    return UserFactory.build()


@pytest.fixture
def user_with_todos() -> Callable:
    """
    Fixture factory to create a user with a specified number of todos (not persisted to database).

    Usage:
        def test_example(user_with_todos):
            user = user_with_todos(todos_size=5)
            assert len(user.todos) == 5
    """

    def _create_user_with_todos(todos_size=3):
        user = UserFactory.build()
        # Manually create the todos list for unit testing (no DB)
        user.todos = [
            TodosFactory.build(owner=user, owner_id=user.id) for _ in range(todos_size)
        ]
        return user

    return _create_user_with_todos


@pytest.fixture
def todo(user):
    """Create a single todo for a user (not persisted to database)."""
    return TodosFactory.build(owner=user, owner_id=user.id)
