import pytest
from ..factories.auth import UserFactory, TodosFactory

# -------------------------------------------------
# Factory-backed fixtures
# -------------------------------------------------
@pytest.fixture
def user():
    return UserFactory()

@pytest.fixture
def user_with_todos():
    return UserFactory(todos__size=3)

@pytest.fixture
def todo(user):
    return TodosFactory(owner=user)