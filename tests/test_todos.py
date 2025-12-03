import pytest

# test_todos.py has been moved to `test/integration/test_todos.py`.
# Keep this shim so CI or local runs that still reference the old path
# won't duplicate or fail — skip the module at collection time.
pytest.skip("moved to test/integration/test_todos.py", allow_module_level=True)
