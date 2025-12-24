from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from ...models import Todos, Users
from ...routers.auth import bcrypt_context
from ...utils.database.connection import Base

import pytest
from .factories.auth import UserFactory
from .factories.todos import TodosFactory

# ======================================================================================
# DATABASE ENGINE CONFIGURATION
# ======================================================================================

# Define a separate SQLite database for integration tests to avoid corrupting
# development or production data.
SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

# StaticPool is used here to ensure that the in-memory/file-based SQLite
# connection remains open and consistent across multiple tests if needed,
# even though individual sessions are closed.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Factory for creating database sessions specifically for the test environment.
# 'bind=engine' hardwires this factory to the test database defined above.
# Any session created by this class will automatically connect to 'testdb.db'.
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Ensure the database schema is fully created before any tests run.
Base.metadata.create_all(bind=engine)


# ======================================================================================
# DEPENDENCY OVERRIDE HELPERS
# ======================================================================================


def override_get_current_user():
    """
    TEST DEPENDENCY: Authentication
    Used to replace 'get_current_user' in FastAPI endpoints.

    By default, this returns None (unauthenticated).
    Advanced integration tests will use 'app.dependency_overrides' to replace
    this with a lambda returning a specific user dictionary.
    """
    # Use the Factory to build the user object, ensuring it matches the model structure.
    # We explicitly set values to maintain backward compatibility with tests expecting
    # these specific credentials.
    user = UserFactory.build(username="codingwithrobytest", id=1, role="admin")

    return {"username": user.username, "id": user.id, "user_role": user.role}


# ======================================================================================
# CORE DATABASE FIXTURE
# ======================================================================================


@pytest.fixture
def test_db_session():
    """
    CORE DATABASE FIXTURE:
    Provides a SQLAlchemy session tied to the test database.

    ISOLATION STRATEGY:
    - We yield a session from the test engine.
    - After the test, we call rollback() to ensure no data is actually committed
      to the testdb.db file, keeping tests isolated and fast.
    """
    # We use TestingSessionLocal() directly here because app.dependency_overrides
    # only affects FastAPI's dependency injection system during a request.
    # Calling get_db_session() directly would still use the production/dev DB.
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        # Ensure the transaction is rolled back so the next test starts fresh
        session.rollback()
        session.close()


# ======================================================================================
# LEGACY FIXTURES (Standard Setup/Teardown Pattern): FOR CODING WITH ROBBY ONLY
# ======================================================================================

# Used
@pytest.fixture
def test_user(test_db_session):
    """
    PROVISIONER: Single Test User
    Creates a user using the unified test_db_session.
    Uses flush() to generate IDs but relies on the session's rollback for cleanup.
    """
    # Check if user already exists (e.g. from a previous test that committed)
    # and delete it to ensure we start with a fresh user state for this fixture.
    existing_user = test_db_session.get(Users, 1)
    if existing_user:
        test_db_session.query(Todos).filter(Todos.owner_id == 1).delete()
        test_db_session.delete(existing_user)
        test_db_session.flush()

    # Use UserFactory to create the object with specific credentials
    user = UserFactory.build(
        id=1,
        username="codingwithrobytest",
        email="codingwithrobytest@email.com",
        first_name="Eric",
        last_name="Roby",
        hashed_password=bcrypt_context.hash("testpassword"),
        role="admin",
        phone_number="(111)-111-1111",
    )

    test_db_session.add(user)
    test_db_session.flush()
    test_db_session.refresh(user)
    return user


@pytest.fixture
def test_todo(test_db_session):
    """
    PROVISIONER: Single Test Todo
    Creates a Todo (and its owner) using the unified test_db_session.
    """
    # Ensure User 1 exists for the FK constraint
    user = test_db_session.get(Users, 1)
    if not user:
        user = UserFactory.build(
            id=1,
            username="codingwithrobytest",
            email="codingwithrobytest@email.com",
            role="admin",
        )
        test_db_session.add(user)
        test_db_session.flush()

    # Passing owner=user explicitly sets owner_id to user.id (1)
    todo = TodosFactory.build(owner=user)
    test_db_session.add(todo)
    test_db_session.flush()
    test_db_session.refresh(todo)
    return todo
