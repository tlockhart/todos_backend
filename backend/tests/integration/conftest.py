import pytest

# Import the generic DB entry fixture and specific fixtures for integration tests
from ..utils.fixtures.integration.db_entry.generic import object_db_entry
from ..utils.fixtures.integration.users import (
    user_db_entry,
    user_with_todos_db_entry,
)
from ..utils.fixtures.integration.db_entry.todos import todo_db_entry
from ..utils.fixtures.integration.db_entry.client import client_with_user
