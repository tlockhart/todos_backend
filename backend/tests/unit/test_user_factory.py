# ======================================================================================
# INFRASTRUCTURE TESTS (Verifying Factories & Fixtures)
# ======================================================================================
# These tests ensure that our test data generation tools are working correctly.


def test_user_fixture_creates_user(user):
    """
    INFRASTRUCTURE TEST:
    - Verifies that the 'user' fixture and UserFactory are configured correctly.
    - This is NOT testing application logic, but rather the test suite's tools.
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
