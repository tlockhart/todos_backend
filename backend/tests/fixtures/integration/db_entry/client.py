import pytest
from fastapi.testclient import TestClient
from ......main import app
from ......utils.database.connection import get_current_user, get_db_session


@pytest.fixture
def client_with_user(test_db_session, user_with_todos_db_entry):
    """
    AUTHENTICATED TEST CLIENT:
    This is the core fixture for integration testing. It performs two critical
    overrides on the FastAPI 'app' using dependency_overrides:

    A) AUTHENTICATION OVERRIDE:
       - It mocks 'get_current_user' to return the user provided by the fixture.
       - This eliminates the need for global variables and bypasses complex
         JWT login flows in tests focused on business logic.

    B) DATABASE SESSION OVERRIDE (The Unified Session):
       - It forces the App to use the EXACT SAME 'db' session as our fixtures.
       - WHY? In SQLite, a second connection cannot see the 'flushed' data of another
         until it is committed. By unifying the session, the API can see the
         Todos we created in the fixtures.

    C) ISOLATION CLEANUP:
       - Calls 'app.dependency_overrides.clear()' in the teardown phase.
       - This is vital: it ensures that the authentication context of one test
         does not leak into the next, which is required for reliable modular test runs.
    """

    # DJANGO SUBSTITUTION:
    # Django's test client has built-in support for forcing login.
    # client.force_login(user_with_todos_db_entry)
    # return client

    # 1. Inject the user into the security dependency layer
    app.dependency_overrides[get_current_user] = lambda: {
        "username": user_with_todos_db_entry.username,
        "id": user_with_todos_db_entry.id,
        "user_role": user_with_todos_db_entry.role,
    }

    # 2. Inject the test transaction into the DB dependency layer
    def get_shared_db_session():
        """
        STRATEGY: Shared/Unified Session.
        - Yields the EXISTING session ('db') from the test fixture.
        - Does NOT close the session (cleanup is handled by the fixture).
        - Critical for SQLite integration tests so the API sees uncommitted data
          (Read-Your-Own-Writes).
        """
        try:
            yield test_db_session
        finally:
            # Lifecycle is managed by the top-level 'db' fixture in conftest.py
            pass

    app.dependency_overrides[get_db_session] = get_shared_db_session

    # 3. Provide the client to the test function
    with TestClient(app) as client:
        yield client

    # 4. Cleanup: Reset the App state for the next test execution
    app.dependency_overrides.clear()
