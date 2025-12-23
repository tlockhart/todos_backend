from sqlalchemy import create_engine, delete
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from ...models import Todos, Users
from ...routers.auth import bcrypt_context
from ...utils.database.connection import Base
from ...main import app
from fastapi import Depends
from fastapi.testclient import TestClient
from ...utils.database.connection import get_db_session

from .factories.auth import UserFactory, TodosFactory
import pytest

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


def override_get_db_session():
    """
    TEST DEPENDENCY: Database Session
    Used to replace 'get_db_session' in FastAPI endpoints.

    STRATEGY: New Session per Request.
    - Creates a fresh SQLAlchemy session for each request.
    - Used as the default global override.
    - Ensures API has DB access when not using the shared 'client_with_user' fixture.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


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
# LEGACY FIXTURES (Standard Setup/Teardown Pattern): FOR CODING WITH ROBBY ONLY
# ======================================================================================


@pytest.fixture
def test_user():
    """
    PROVISIONER: Single Test User
    Creates a user using the TestingSessionLocal and commits it to the database.

    Why Commit here instead of Flush?
    - These legacy fixtures are designed for tests that don't necessarily
      use the unified session strategy. They ensure data persists long enough
      for a standard TestClient to find it.

    Cleanup: Uses a raw engine connection to delete all Users after the test
    finishes to ensure a clean state for the next run.
    """
    # Use UserFactory to create the object, but override fields to match
    # the specific credentials expected by existing tests (e.g. test_users.py)
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

    db = TestingSessionLocal()
    # Pre-cleanup: Ensure no conflicting users exist from previous tests (e.g. test_todo)
    # This prevents UNIQUE constraint failed: users.username
    db.execute(delete(Todos))
    db.execute(delete(Users))
    db.commit()

    db.add(user)
    db.commit()
    db.refresh(user)

    yield user

    # Cleanup: Hard delete all users from the test table
    with engine.connect() as connection:
        connection.execute(delete(Todos))
        connection.execute(delete(Users))
        connection.commit()


@pytest.fixture
def test_todo():
    """
    PROVISIONER: Single Test Todo
    Ensures the Todos table is empty, creates one Todo, and commits it.

    Cleanup: Explicitly deletes all Todos after the test completes.
    Note: This fixture is primarily used for tests that don't rely on
    complex relationship factories.
    """
    db = TestingSessionLocal()
    try:
        # Pre-test cleanup to ensure no ID collisions
        db.execute(delete(Todos))
        db.commit()

        # Ensure User 1 exists for the FK constraint and auth override
        user = db.get(Users, 1)
        if not user:
            user = UserFactory.build(id=1, username="codingwithrobytest", role="admin")
            # Clean up any existing users to prevent Unique violations (e.g. email)
            # This handles cases where a user exists with a conflicting email but different ID
            db.execute(delete(Users))
            db.commit()

            user = UserFactory.build(
                id=1,
                username="codingwithrobytest",
                email="codingwithrobytest@email.com",
                role="admin",
            )
            db.add(user)
            db.commit()

        # Passing owner=user explicitly sets owner_id to user.id (1) and prevents
        # the SubFactory from creating a new random user.
        todo = TodosFactory.build(owner=user)
        db.add(todo)
        db.commit()
        # Refresh to populate DB-generated fields (like IDs)
        db.refresh(todo)
    finally:
        db.close()

    yield todo

    # Final cleanup to prevent data leakage
    db = TestingSessionLocal()
    try:
        db.execute(delete(Todos))
        db.commit()
    finally:
        db.close()
