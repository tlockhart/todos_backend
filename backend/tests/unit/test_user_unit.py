# UNIT TESTS — User fixture only

def test_user_fixture_creates_user(user):
    """
    UNIT:
    - UserFactory creates a valid User
    """

    assert user.id is not None
    assert user.username
    assert user.email
    assert user.is_active is True
    assert user.todos == []


def test_user_with_todos_fixture(user_with_todos):
    """
    UNIT:
    - RelatedFactoryList works
    - Relationship is wired correctly
    """
    user = user_with_todos(todos_size=3)

    assert user.id is not None
    assert len(user.todos) == 3

    for todo in user.todos:
        assert todo.owner_id == user.id
        assert todo.owner is user