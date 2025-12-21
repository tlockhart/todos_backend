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
    
    This function provides a fresh SQLAlchemy session from the TestingSessionLocal factory.
    It follows the FastAPI dependency pattern: yield the session, then close it.
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
    return None


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
    user = Users(
        username="codingwithrobytest",
        email="codingwithrobytest@email.com",
        first_name="Eric",
        last_name="Roby",
        hashed_password=bcrypt_context.hash("testpassword"),
        role="admin",
        phone_number="(111)-111-1111",
    )
    
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    db.refresh(user)
    
    yield user
    
    # Cleanup: Hard delete all users from the test table
    with engine.connect() as connection:
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
    todo = Todos(
        title="Learn to code!",
        description="Need to learn everyday!",
        priority=5,
        complete=False,
        owner_id=1,
    )

    db = TestingSessionLocal()
    try:
        # Pre-test cleanup to ensure no ID collisions
        db.execute(delete(Todos))
        db.commit()
        
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