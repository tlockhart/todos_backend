import pytest

# ======================================================================================
# 1. CORE DATABASE UTILITY FIXTURE
# ======================================================================================


# DJANGO SUBSTITUTION: This fixture is generally NOT needed in Django.
# factory_boy's DjangoModelFactory handles persistence automatically via .create().
# You would simply call UserFactory.create() instead of object_db_entry(UserFactory).
@pytest.fixture
def object_db_entry(test_db_session):
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
        test_db_session.add(obj)

        # Flush to generate Primary Keys (IDs) and sync with the database
        test_db_session.flush()
        # Refresh ensures the object is updated with any DB-generated defaults
        test_db_session.refresh(obj)
        return obj

    return create_entry
