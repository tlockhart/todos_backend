# UNIT TESTS — Todos fixture only

def test_todo_fixture_creates_todo(todo):
    """
    UNIT:
    - TodoFactory creates a valid Todo
    """
    # Not a db object
    # assert todo.id is not None
    assert todo.title
    assert todo.description
    assert 1 <= todo.priority <= 5
    assert todo.complete is False
    # assert todo.owner_id == todo.owner.id