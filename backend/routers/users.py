from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status

from ..models import Users
from ..utils.database.connection import get_db_session

from ..utils.database.connection import get_current_user
from passlib.context import CryptContext

# ⬅ every route in this file gets prefixed with /user
router = APIRouter(prefix="/user", tags=["user"])

db_dependency = Annotated[Session, Depends(get_db_session)]
user_dependency = Annotated[dict, Depends(get_current_user)]
# bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
# Setup argon2 or pbkdf2_sha256, which don’t have the 72-byte limit:
bcrypt_context = CryptContext(
    schemes=["argon2"], deprecated="auto"  # instead of bcrypt
)


# Request Body for change password: Pssword Verification Model
class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


# See all user about themselves
@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.get(Users, user.get("id"))


# Change password
@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency, db: db_dependency, user_verification: UserVerification
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    user_model = db.get(Users, user.get("id"))

    if not bcrypt_context.verify(
        user_verification.password, user_model.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Error on password change")
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()


# Change phone_number:
@router.put("/phonenumber/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(
    user: user_dependency, db: db_dependency, phone_number: str
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    user_model = db.get(Users, user.get("id"))

    # Update phone_number
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()


# Change phone_number using query parameter:
@router.put("/phonenumber", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number_query(
    user: user_dependency, db: db_dependency, phone_number: str = Query(...)
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    user_model = db.get(Users, user.get("id"))
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()
