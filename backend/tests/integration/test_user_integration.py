from datetime import timedelta
from jose import jwt

from backend.routers.auth import (
    authenticate_user,
    create_access_token,
    SECRET_KEY,
    ALGORITHM,
)

# -------------------------------------------------
# INTEGRATION TEST
# -------------------------------------------------
def test_authenticate_user(db, user):
    """
    INTEGRATION:
    - DB-backed authentication
    """

    authenticated = authenticate_user(
        db,
        username=user.username,
        password=user.hashed_password,
    )

    assert authenticated is not None
    assert authenticated.id == user.id


# -------------------------------------------------
# INTEGRATION TEST
# -------------------------------------------------
def test_create_access_token_with_real_user(user):
    """
    INTEGRATION:
    - Token created from real User
    """

    token = create_access_token(
        username=user.username,
        user_id=user.id,
        role=user.role,
        expires_delta=timedelta(minutes=15),
    )

    decoded = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
        options={"verify_signature": False},
    )

    assert decoded["sub"] == user.username
    assert decoded["id"] == user.id
    assert decoded["role"] == user.role