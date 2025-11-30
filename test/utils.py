from sqlalchemy import create_engine, delete
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..models import Todos, Users
from ..routers.auth import bcrypt_context
from ..utils.database.connection import Base
from ..main import app
from fastapi.testclient import TestClient
client = TestClient(app)

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

# Add Todo Fixture
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
        
# Add User Fixture to add one user to the database and delete when done
@pytest.fixture
def test_user():
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
    yield user
    with engine.connect() as connection:
        connection.execute(delete(Users))
        connection.commit() 