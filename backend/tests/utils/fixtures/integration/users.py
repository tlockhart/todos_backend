import pytest
from ...factories.auth import UserFactory, TodosFactory


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
        object_db_entry(TodosFactory, owner=user, owner_id=user.id)

    return user
