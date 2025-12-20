from todos_backend.utils.jwt import SECRET_KEY, ALGORITHM, create_access_token
from jose import jwt

def generate_test_token(user_id: int, username: str, role: str = "admin") -> str:
    payload = {
        "sub": username,
        "id": user_id,
        "role": role,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token