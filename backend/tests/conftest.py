import pytest
from ..main import app
from ..utils.database.connection import get_db_session, get_current_user, oauth2_bearer
from .utils.test_db_setup import (
    override_get_current_user,
    TestingSessionLocal,
    test_db_session,
)

# Unit test fixtures (no DB interaction)
from .utils.fixtures.user_unit import user, user_with_todos, todo
from .utils.fixtures.integration.users import user_db_entry
from .utils.fixtures.integration.generic import object_db_entry
from .utils.fixtures.integration.db_entry.todos import todo_db_entry


# --------------------------------------------------------------------------------------
# 1. DATABASE SESSION FIXTURE
# --------------------------------------------------------------------------------------
# This fixture has been moved to tests/utils/test_db_setup.py for better organization.


# --------------------------------------------------------------------------------------
# 2. GLOBAL OVERRIDES (Optional / Minimal)
# --------------------------------------------------------------------------------------
@pytest.fixture(autouse=True)
def base_dependency_overrides(test_db_session):
    """
    GLOBAL DEPENDENCY OVERRIDE: Authentication
    This is an `autouse` fixture, meaning it runs automatically before every test.

    PURPOSE:
    Its main role is to support integration tests that make API calls to protected
    endpoints. It overrides the `oauth2_bearer` dependency for the entire application.

    HOW IT WORKS:
    Instead of requiring a real, generated JWT for authenticated endpoints, this
    override replaces the token validation logic with a simple function that
    returns a "fake-token" string. This effectively bypasses the authentication
    layer, allowing tests to focus on the endpoint's logic without the overhead
    of generating valid tokens. This is crucial for tests involving database
    operations on protected routes, as it simplifies the test setup significantly.
    """
    # DJANGO SUBSTITUTION: Remove this fixture.
    # Django tests use client.force_login(user) to bypass auth for specific tests.
    # Global overrides are generally not used in the same way.
    # This is safe to keep global as it's a constant mock
    app.dependency_overrides[oauth2_bearer] = lambda: "fake-token"
    app.dependency_overrides[get_db_session] = lambda: test_db_session

    yield

    # We do NOT clear here if using client_with_user, as that fixture
    # handles its own lifecycle. If we clear here, we might wipe overrides
    # that the test is currently using.
