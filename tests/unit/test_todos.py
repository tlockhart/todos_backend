"""Unit tests for Todos model (file named `test_todos.py` because it's already
under `test/unit` — no need for the `_unit` suffix).
"""

from todos_backend.models import Todos


def test_todos_model_instantiation():
    todo = Todos(
        title="write unit test",
        description="Make sure model creates attributes without DB",
        priority=3,
        complete=False,
        owner_id=42,
    )

    assert todo.title == "write unit test"
    assert todo.description == "Make sure model creates attributes without DB"
    assert todo.priority == 3
    assert todo.complete is False
    assert todo.owner_id == 42
