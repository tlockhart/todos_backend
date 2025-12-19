import pytest
from ..factories.auth import UserFactory, TodosFactory

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
        db.flush()  # Use flush instead of commit to keep in transaction
        db.refresh(obj)
        created_objects.append(obj)
        return obj

    yield create_entry

    # Cleanup - delete in reverse order
    for obj in reversed(created_objects):
        db.delete(obj)
    db.commit()


# -------------------------------------------------
# Specific fixtures using the generic object_db_entry
# -------------------------------------------------
@pytest.fixture
def user_db_entry(object_db_entry):
    """Create a user and persist to database."""
    new_user = object_db_entry(UserFactory)
    new_user._plain_password = "Password123!"  # transient attribute for tests
    return new_user


@pytest.fixture
def user_with_todos_db_entry(object_db_entry):
    """Create a user with 3 todos and persist to database."""
    user = object_db_entry(UserFactory)
    
    for _ in range(3):
        object_db_entry(TodosFactory, owner=user, owner_id=user.id)
    
    return user


@pytest.fixture
def todo_db_entry(object_db_entry, user_db_entry):
    """Create a single todo for a user and persist to database."""
    return object_db_entry(TodosFactory, owner=user_db_entry, owner_id=user_db_entry.id)
