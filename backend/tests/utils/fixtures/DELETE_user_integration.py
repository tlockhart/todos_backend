# import pytest
# # from todos_backend.utils.jwt import SECRET_KEY, ALGORITHM
# from jose import jwt

# # connect to .env
# from dotenv import load_dotenv
# import os

# load_dotenv()  # loads variables from .env

# SECRET_KEY = os.getenv("SECRET_KEY")
# ALGORITHM = os.getenv("ALGORITHM")

# @pytest.fixture
# def auth_token(user, user_id=1):
#     payload = {"sub": user.username, "id": user_id, "role": "admin"}
#     token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
#     return {"Authorization": f"Bearer {token}"}

