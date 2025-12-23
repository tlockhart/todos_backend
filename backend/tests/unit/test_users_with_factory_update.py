from ..utils import *
from ...utils.database.connection import get_current_user
from ..utils.db_connections import override_get_current_user, test_user
from ...main import app
from fastapi.testclient import TestClient
from fastapi import status
import pytest

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_user_overrides():
    app.dependency_overrides[get_current_user] = override_get_current_user
    yield
    del app.dependency_overrides[get_current_user]


# Roby called all these Unit Tests. But sinc testing User
# Fixture Model creation and get route, it is integration.
def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == test_user.username
    assert response.json()["email"] == test_user.email
    assert response.json()["role"] == test_user.role
    assert response.json()["phone_number"] == test_user.phone_number
    assert response.json()["first_name"] == test_user.first_name
    assert response.json()["last_name"] == test_user.last_name


def test_change_password_success(test_user):
    response = client.put(
        "/user/password",
        json={"password": "testpassword", "new_password": "new_password"},
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    response = client.put(
        "/user/password",
        json={"password": "wrong_password", "new_password": "newpassword"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Error on password change"}


def test_change_phone_number_success(test_user):
    response = client.put("/user/phonenumber/2222222222")
    assert response.status_code == status.HTTP_204_NO_CONTENT
