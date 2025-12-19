import pytest
from ..main import app
from ..utils.database.connection import get_db_session, get_current_user
from .utils.db_connections import override_get_db_session, override_get_current_user, TestingSessionLocal

# Unit test fixtures (no DB interaction)
from .utils.fixtures.user import user, user_with_todos, todo


# -------------------------------------------------
# GLOBAL FastAPI dependency override (autouse)
# -------------------------------------------------
@pytest.fixture(autouse=True, scope="session")
def override_db_dependency():
    """Automatically override get_db_session for all tests."""
    app.dependency_overrides[get_db_session] = override_get_db_session
    app.dependency_overrides[get_current_user] = override_get_current_user
    
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
        try:
            next(db_gen)
        except StopIteration:
            pass