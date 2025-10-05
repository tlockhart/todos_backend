from datetime import timedelta, datetime, timezone
from typing import Annotated

# Step 1 of 2: APIRouter allows us to route from main.py API file to our auth.py file
from fastapi import APIRouter, Depends, HTTPException

from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal

# Import user model
from models import Users

from passlib.context import CryptContext

# OAUTH 2.0 for PasswordReqeustForm, BearerToken
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

# JWT
from jose import jwt, JWTError

# connect to .env
from dotenv import load_dotenv
import os

load_dotenv()  # loads variables from .env

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


# ⬅ every route in this file gets prefixed with /auth
# Separate the /auth routes from default routes in todos:
router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

# Setup argon2 or pbkdf2_sha256, which don’t have the 72-byte limit:
bcrypt_context = CryptContext(schemes=["argon2"],  # instead of bcrypt
    deprecated="auto")

# Bearer token: Verify token for the current user, using /auth/token route => calls /token route below
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

# Pydantic Class for Validation
class CreateUserRequest(BaseModel):
    # id auto
    # is_active: auto
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str

# Token model
class Token(BaseModel):
    access_token: str
    token_type: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

# Method passed username and password, and db to verfity password matches users hashed_password
def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

# create token
def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.now(timezone.utc) + expires_delta
    # update jwt with datetime
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# Validate the access_token received during login, using dependency injection of oauth2bearer
# IMPORTANT: Each request to todo or any authenticated routes will call get_current_user to verify if user has a valid token
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        # User secret_key and algorithm to decode our token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate username or user_id.')
        return {'username': username, 'id': user_id, 'user_role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate JWT or role.')
"""
Auth Routes
"""
# Step 2 of 2: No /auth required since all routers are prefixed with /auth, see above
# @router.post("/auth/")
# async def create_user():
#     return {'user': 'authenticated'}
# db_dependency - dependency injection from our db
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      create_user_request: CreateUserRequest):
    # Create a user, ** will not work, because password is a hashpasswd in model
    #create_user_model = Users(##create_user_request.dict())
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        # Encrypt the password
        hashed_password=bcrypt_context.hash(create_user_request.password),
        # hashed_password=create_user_request.password,
        is_active=True,
        phone_number=create_user_request.phone_number
    )

    # Create new user
    db.add(create_user_model)
    # commit to database
    db.commit()
    db.refresh(create_user_model)  # 👈 ensures model has ID populated
    return create_user_model

# accesstoken login: returns JWT TOKEN
# response_model should match the Token model above
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependency):
    # Call verify user password
    user = authenticate_user(form_data.username, form_data.password, db)
    # If no user raise an error
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')
    token = create_access_token(user.username, user.id, user.role, timedelta(hours=1))

    return {'access_token': token, 'token_type': 'bearer'}







