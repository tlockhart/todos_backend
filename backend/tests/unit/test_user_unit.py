from ...models import Users
# ======================================================================================
# INFRASTRUCTURE TESTS (Verifying Factories & Fixtures)
# ======================================================================================
# These tests ensure that our test data generation tools are working correctly.


def test_user_fixture_creates_user(user):
    """
    UNIT:
    - UserFactory creates a valid User
    """
    # Not a db object
    # assert user.id is not None
    assert user.username
    assert user.email
    assert user.is_active is True
    # DJANGO SUBSTITUTION:
    # Django reverse relationships are Managers, not lists. Accessing 'user.todos' on an
    # unsaved instance usually raises a ValueError.
    assert user.todos == []


def test_user_with_todos_fixture(user_with_todos):
    """
    UNIT:
    - RelatedFactoryList works
    - Relationship is wired correctly
    """
    user = user_with_todos(todos_size=3)

    # assert user.id is not None
    # DJANGO SUBSTITUTION:
    # If using standard Django ORM: assert user.todos.count() == 3
    assert len(user.todos) == 3

    for todo in user.todos:
        # assert todo.owner_id == user.id
        assert todo.owner is user


# ======================================================================================
# MODEL TESTS (Verifying Business Logic)
# ======================================================================================
def test_user_model_instantiation():
    """
    UNIT:
    - Direct Users model instantiation (no Factory).
    - Verifies the model definition itself works as expected.
    """
    # DJANGO SUBSTITUTION:
    # from django.contrib.auth import get_user_model
    # User = get_user_model()
    # user = User(username="testuser", email="test@example.com", ...)
    # Note: Django models don't typically accept 'hashed_password' in __init__.
    # You would instantiate with no password or a plain one, then call user.set_password().
    user = Users(
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_secret",
        role="admin",
        is_active=True,
    )

    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.role == "admin"
    assert user.is_active is True
