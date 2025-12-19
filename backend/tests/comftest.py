import pytest
from backend.main import app
from backend.utils.database.connection import get_db_session
from .utils import override_get_db_session, override_get_current_user, TestingSessionLocal, test_todo

from ..utils.fixtures.user import user, user_with_todos, todo
# -------------------------------------------------
# GLOBAL FastAPI dependency override (autouse)
# -------------------------------------------------
@pytest.fixture(autouse=True, scope="session")
def override_db_dependency():
    """Automatically override get_db_session for all tests."""
    app.dependency_overrides[get_db_session] = override_get_db_session
    yield
    app.dependency_overrides.clear()

# -------------------------------------------------
# Database session fixture
# -------------------------------------------------
@pytest.fixture
def db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()