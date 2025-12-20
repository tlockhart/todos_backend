import pytest
from ..main import app
from ..utils.database.connection import get_db_session, get_current_user
from .utils.db_connections import override_get_db_session, override_get_current_user, TestingSessionLocal
from ..utils.database.connection import oauth2_bearer
from fastapi.security import OAuth2PasswordBearer
# Unit test fixtures (no DB interaction)
from .utils.fixtures.user_unit import user, user_with_todos, todo


# -------------------------------------------------
# GLOBAL FastAPI dependency override (autouse)
# -------------------------------------------------
@pytest.fixture(autouse=True, scope="session")
def override_db_dependency():
    """Automatically override get_db_session for all tests."""
    """get_db_session override: All tests will use the SQLite 
    in-memory or test file DB, so your integration tests won’t 
    touch MySQL."""
    app.dependency_overrides[get_db_session] = override_get_db_session
    """get_current_user override: Your override_get_current_user fixture 
    still returns the test user from the SQLite test DB, so routes that 
    use the token will now behave as if the token is valid."""
    app.dependency_overrides[get_current_user] = override_get_current_user
    """ensures any route depending on OAuth2PasswordBearer receives 
    "fake-token" instead of trying to hit the real token flow."""
    app.dependency_overrides[oauth2_bearer] = lambda: "fake-token"
    yield

    app.dependency_overrides.clear()

# -------------------------------------------------
# Database session fixture
# -------------------------------------------------
@pytest.fixture
def db():
    """
    Provides a test database session for integration tests.
    Uses the same overridden get_db_session that FastAPI uses.
    """
    db_gen = override_get_db_session()
    session = next(db_gen)
    try:
        yield session
        
    finally:
        # NOTE: TEST ISOLATION: REMOVE EVERYTHING CREATED DUING TEST
        session.rollback()   # 🔑 THIS IS THE FIX
        session.close()