import pytest
from ..factories.auth import UserFactory, TodosFactory
from ..db_connections import set_test_user
from ....main import app
from ....utils.database.connection import get_current_user, get_db_session
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

# -------------------------------------------------
# Generic database fixture - insert any factory object
# -------------------------------------------------
@pytest.fixture
def object_db_entry(db):
    """
    Generic fixture to insert any factory object into the test database.
    
    Usage:
        user = object_db_entry(UserFactory)
        todo = object_db_entry(TodosFactory, owner=user)
    """
    created_objects = []

    def create_entry(factory_class, **kwargs):
        """Create and persist a factory object to the database."""
        obj = factory_class.build(**kwargs)
        db.add(obj)
        # db.flush()  # Use flush instead of commit to keep in transaction
        # db.commit()        # ← Error: Causing duplicate entries
        db.flush()  # FIX: keep in transaction without committing
        db.refresh(obj)
        created_objects.append(obj)
        return obj

    yield create_entry


# -------------------------------------------------
# Specific fixtures using the generic object_db_entry
# -------------------------------------------------
@pytest.fixture
def user_db_entry(object_db_entry):
    """Create a user and persist to database."""
    new_user = object_db_entry(UserFactory)
    new_user._plain_password = "Password123!"  # transient attribute for tests
    # Set the _plain_password on the global user
    set_test_user(new_user)
    return new_user

# Integration Fixtures:

@pytest.fixture
def user_with_todos_db_entry(object_db_entry):
    """Create a user with 3 todos and persist to database."""
    user = object_db_entry(UserFactory)
    # set test user to be the user in the UserFactory
    set_test_user(user)
    for _ in range(3):
        # Use global user
        object_db_entry(TodosFactory, 
                        owner=user, 
                        owner_id=user.id)
    
    return user


# @pytest.fixture
# def todo_db_entry(object_db_entry, user_db_entry):
#     """Create a single todo for a user and persist to database."""
#     return object_db_entry(TodosFactory, owner=user_db_entry, owner_id=user_db_entry.id)

@pytest.fixture
def todo_db_entry(object_db_entry, user_with_todos_db_entry):
    """Create a single todo for the overridden test user."""
    return object_db_entry(
        TodosFactory,
        owner=user_with_todos_db_entry,
        owner_id=user_with_todos_db_entry.id
    )


# -----------------------------------------------------------------
# Fixture to provide a test client with an authenticated user
# NOTE: USE IN ALL TEST REQUIRING AUTH
# -----------------------------------------------------------------
@pytest.fixture
def client_with_user(user_with_todos_db_entry):
    client = TestClient(app)
    # Override dependency to return the user directly
    # Use global user
    app.dependency_overrides[get_current_user] = lambda: {
        "username": user_with_todos_db_entry.username,
        "id": user_with_todos_db_entry.id,
        "user_role": user_with_todos_db_entry.role
    }
    yield client
    app.dependency_overrides.clear()
    