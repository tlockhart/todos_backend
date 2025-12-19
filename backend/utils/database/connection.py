from typing import Annotated

# Step 1 of 2: APIRouter allows us to route from main.py API file to our auth.py file
from fastapi import Depends, HTTPException, status

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# connect to .env
from dotenv import load_dotenv
import os

# JWT
from jose import jwt, JWTError

# OAUTH 2.0 for PasswordReqeustForm, BearerToken
from fastapi.security import OAuth2PasswordBearer

# Bearer token: Verify token for the current user, using /auth/token route => calls /token route below
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

load_dotenv()  # loads variables from .env

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# Validate the access_token received during login, using dependency injection of oauth2bearer
# IMPORTANT: Each request to todo or any authenticated routes will call get_current_user to verify if user has a valid token
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        # User secret_key and algorithm to decode our token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate username or user_id.",
            )
        return {"username": username, "id": user_id, "user_role": user_role}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate JWT or role.",
        )

# URL to create a location for the database on our fastAPI application
# DB is in this directory of our todo app
# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
SQLALCHEMY_DATABASE_URL = (
    "mysql+pymysql://root:password@127.0.0.1:3306/TodoApplicationDatabase"
)


# create and engine to open up a db connection to use our database
# Connect Arguments passed to engine define connection to a db.  Only one thread will communicate with sql for independent requests
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
engine = create_engine(SQLALCHEMY_DATABASE_URL)


# Create an instance of sessionLocal from sessionmaker, bind to the engine created do not auto commit or flush data
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create SQL DB  object that we can interact with
# Used to create database tables and interact with them
Base = declarative_base()

"""
Create and return a databas session object
"""


def get_db_session():
    session = SessionLocal()
    try:
        # Only the code prior to and including the yield statement executed, before sending a response
        yield session
        # After response is delivered close db
    finally:
        session.close()
