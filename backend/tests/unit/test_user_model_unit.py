from ...models import Users


# ======================================================================================
# MODEL TESTS (Verifying Model Structure)
# ======================================================================================
def test_user_model_instantiation():
    """
    UNIT:
    - Direct Users model instantiation (no Factory).
    - Verifies the model definition itself works as expected.
    """
    # DJANGO SUBSTITUTION:
    # from django.contrib.auth import get_user_model
    # User = get_user_model()
    # user = User(username="testuser", email="test@example.com", ...)
    # Note: Django models don't typically accept 'hashed_password' in __init__.
    # You would instantiate with no password or a plain one, then call user.set_password().
    user = Users(
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_secret",
        role="admin",
        is_active=True,
    )

    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.role == "admin"
    assert user.is_active is True
    assert hasattr(user, "hashed_password")
