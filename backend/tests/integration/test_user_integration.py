from datetime import timedelta
from jose import jwt

from ...routers.auth import (
    authenticate_user,
    create_access_token,
    SECRET_KEY,
    ALGORITHM,
)

# -------------------------------------------------
# INTEGRATION TEST
# -------------------------------------------------
def test_authenticate_user(test_db_session, user_db_entry):
    """
    INTEGRATION:
    - DB-backed authentication
    """

    # DJANGO SUBSTITUTION:
    # from django.contrib.auth import authenticate
    # authenticated = authenticate(username=user_db_entry.username, password=user_db_entry._plain_password)
    # Note: Django's authenticate() does not require a db session argument.
    user_db_entry = user_db_entry()
    authenticated = authenticate_user(
        test_db_session,
        username=user_db_entry.username,
        # password=user_db_entry.hashed_password,
        password=user_db_entry._plain_password,  # <-- plaintext, not hash
    )

    assert authenticated is not None
    assert authenticated.id == user_db_entry.id


# -------------------------------------------------
# INTEGRATION TEST
# -------------------------------------------------
def test_create_access_token_with_real_user(user_db_entry):
    """
    INTEGRATION:
    - Token created from real User
    """

    # DJANGO SUBSTITUTION:
    # Django does not have built-in JWT support. If using 'djangorestframework-simplejwt':
    # from rest_framework_simplejwt.tokens import RefreshToken
    # token = str(RefreshToken.for_user(user_db_entry).access_token)
    user_db_entry = user_db_entry()
    token = create_access_token(
        username=user_db_entry.username,
        user_id=user_db_entry.id,
        role=user_db_entry.role,
        expires_delta=timedelta(minutes=15),
    )

    decoded = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
        options={"verify_signature": False},
    )

    assert decoded["sub"] == user_db_entry.username
    assert decoded["id"] == user_db_entry.id
    assert decoded["role"] == user_db_entry.role