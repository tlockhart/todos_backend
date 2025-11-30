from .utils import *
from ..utils.database.connection import get_current_user, get_db_session
from fastapi import status

app.dependency_overrides[get_db_session] = override_get_db_session
app.dependency_overrides[get_current_user] = override_get_current_user

# Roby called all these Unit Tests. But sinc testing User 
# Fixture Model creation and get route, it is integration.
def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() ['username'] == 'codingwithrobytest'
    assert response.json() ['email'] == 'codingwithrobytest@email.com'
    assert response.json() ['role'] == 'admin'
    assert response.json() ['phone_number'] == '(111)-111-1111'
    assert response.json() ['first_name'] == 'Eric' 
    assert response.json() ['last_name'] == 'Roby'
    
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
    assert response.json() == {'detail': 'Error on password change'}
    
def test_change_phone_number_success(test_user):
    response = client.put(
        "/user/phonenumber/2222222222"
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
