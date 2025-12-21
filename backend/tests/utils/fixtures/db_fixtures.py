import pytest
from fastapi.testclient import TestClient
from ....main import app
from ....utils.database.connection import get_current_user, get_db_session
from ..factories.auth import UserFactory, TodosFactory

# ======================================================================================
# 1. CORE DATABASE UTILITY FIXTURE
# ======================================================================================

@pytest.fixture
def object_db_entry(db):
    """
    GENERIC DATABASE INJECTOR:
    This fixture acts as a functional bridge between 'factory_boy' (data generation) 
    and our SQLAlchemy test session (data persistence).

    TECHNICAL STRATEGY:
    - It uses 'db.add()' and 'db.flush()' instead of 'db.commit()'.
    - WHY? 'flush()' pushes the data to the database so it generates IDs (Primary Keys),
      but it keeps the database transaction open.
    - This allows the parent 'db' fixture to roll back the entire transaction after 
      each test, ensuring a perfectly clean database for the next test without 
      manual deletion logic.
    """
    def create_entry(factory_class, **kwargs):
        """Builds, persists, and refreshes a database model from a factory."""
        # Use build() to create the object instance in memory
        obj = factory_class.build(**kwargs)
        db.add(obj)
        
        # Flush to generate Primary Keys (IDs) and sync with the database
        db.flush()
        # Refresh ensures the object is updated with any DB-generated defaults
        db.refresh(obj)
        return obj

    return create_entry


# ======================================================================================
# 2. DATA PROVISIONING FIXTURES (The "Arrange" Phase)
# ======================================================================================

@pytest.fixture
def user_db_entry(object_db_entry):
    """
    BASIC USER PROVISIONER:
    Creates a single User record in the database.
    - Primary Use: Auth integration tests (e.g., test_authenticate_user).
    - Attribute: Adds '_plain_password' to the object. Because the DB only stores 
      hashes, this provides the test with the raw password needed for login attempts.
    """
    new_user = object_db_entry(UserFactory)
    new_user._plain_password = "Password123!"
    return new_user

@pytest.fixture
def user_with_todos_db_entry(object_db_entry):
    """
    COMPLEX STATE PROVISIONER:
    Creates a User and automatically populates the database with 3 associated Todo items.
    - Primary Use: Provides the default data context for authenticated API tests.
    - Linking: Explicitly links Todos to the User's ID to ensure Foreign Key integrity.
    """
    user = object_db_entry(UserFactory)
    
    # Create related resources linked to the user we just created
    for _ in range(3):
        object_db_entry(
            TodosFactory, 
            owner=user, 
            owner_id=user.id
        )
    
    return user

@pytest.fixture
def todo_db_entry(object_db_entry, user_with_todos_db_entry):
    """
    SINGLE RESOURCE PROVISIONER:
    Creates exactly one Todo for the user provided by 'user_with_todos_db_entry'.
    - Primary Use: Tests for specific resource endpoints (e.g., GET /todos/todo/{id}).
    - This ensures the resource being tested is owned by the logged-in user.
    """
    return object_db_entry(
        TodosFactory,
        owner=user_with_todos_db_entry,
        owner_id=user_with_todos_db_entry.id
    )


# ======================================================================================
# 3. FASTAPI INTEGRATION FIXTURES (The "Unified Session" Strategy)
# ======================================================================================

@pytest.fixture
def client_with_user(db, user_with_todos_db_entry):
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
    
    # 1. Inject the user into the security dependency layer
    app.dependency_overrides[get_current_user] = lambda: {
        "username": user_with_todos_db_entry.username,
        "id": user_with_todos_db_entry.id,
        "user_role": user_with_todos_db_entry.role
    }

    # 2. Inject the test transaction into the DB dependency layer
    def override_get_db():
        try:
            yield db
        finally:
            # Lifecycle is managed by the top-level 'db' fixture in conftest.py
            pass

    app.dependency_overrides[get_db_session] = override_get_db

    # 3. Provide the client to the test function
    with TestClient(app) as client:
        yield client
    
    # 4. Cleanup: Reset the App state for the next test execution
    app.dependency_overrides.clear()