# import engine
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from starlette import status
from ..models import Todos

from ..utils.database.connection import Base, get_db_session, get_current_user
from ..main import app

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


# Change dependencies on the client
app.dependency_overrides[get_db_session] = override_get_db_session
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


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
        db.query(Todos).delete(synchronize_session=False)
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
        db.query(Todos).delete(synchronize_session=False)
        db.commit()
    finally:
        db.close()

    # Drop everything
    # with engine.begin() as conn:
    #     conn.run_sync(Base.metadata.drop_all)


# Pass the test_todo into the test
def test_read_all_authenticated(test_todo):
    # ensure the fixture created a todo and the endpoint returns it
    response = client.get("/todos")
    assert response.status_code == status.HTTP_200_OK
    # Make assertions about the returned todo fields (ignore auto-generated id)
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    item = data[0]
    assert item["title"] == "Learn to code!"
    assert item["description"] == "Need to learn everyday!"
    assert item["priority"] == 5
    assert item["complete"] is False
    assert item["owner_id"] == 1

    # --- also assert the returned JSON equals the fixture's serialized model ---
    from sqlalchemy import inspect

    def model_to_dict(obj):
        # convert SQLAlchemy ORM instance to a dict of column values
        return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

    expected = model_to_dict(test_todo)
    assert item == expected
