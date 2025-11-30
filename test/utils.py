from sqlalchemy import create_engine, delete
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..models import Todos
from ..utils.database.connection import Base

import pytest

# Create a new sqlite database (testdb.db) in the root project directory (fastAPI):
SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Mock user
def override_get_current_user():
    return {"username": "tlockhart6", "id": 1, "user_role": "admin"}

# Add Fixture
@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learn to code!",
        description="Need to learn everyday!",
        priority=5,
        complete=False,
        owner_id=1,
    )

    # Create a session, clear any existing rows and add the fixture todo so test starts clean
    db = TestingSessionLocal()
    try:
        db.execute(delete(Todos))
        db.commit()
        db.add(todo)
        db.commit()
        # refresh so the ORM instance has generated fields (id, etc.) populated
        db.refresh(todo)
    finally:
        db.close()
    yield todo

    # Delete all rows in Todos table using an ORM session (SQLAlchemy 2.0 friendly)
    # ensure tables are clean after test
    db = TestingSessionLocal()
    try:
        db.execute(delete(Todos))
        db.commit()
    finally:
        db.close()