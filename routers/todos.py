from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

# Step 1 of 2: APIRouter allows us to route from main.py API file to our auth.py file
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status

from ..models import Todos

"""
Import get_current_user from auth (to validate JWT, and turn into username, id, payload), 
see below# The leading dot (.) tells Python to import from the current package/module directory
"""
from ..utils.database.connection import get_db_session, get_current_user



# Use APIRouter to define routes
router = APIRouter(prefix="/todos", tags=["todos"])

# Depends - dependency injection ( do something b4 exe)
# Run get_db_session() first, and inject the returned db Session into the endpoint.
db_dependency = Annotated[Session, Depends(get_db_session)]
# Run get_current_user() first, and inject the returned users access token.
user_dependency = Annotated[dict, Depends(get_current_user)]

"""
Pydantic Validations
"""


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool
    # sqlalchemy will auto increment id


"""
TODOS: API INPUTS
"""


# Get all todos, by user
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    # Pass in the required model to the query function
    return db.query(Todos).filter(Todos.owner_id == user.get("id")).all()


"""
@router.get("/", status_code=status.HTTP_200_OK)
# async def read_all(db: Annotated[Session, Depends(get_db_session)]):
async def read_all(db: db_dependency):
    # Pass in the required model to the query function
    return db.query(Todos).all()
"""


# todo Path Parameter, get todo by todo_id, with user validation
@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(
    # user session from user_dependency
    user: user_dependency,
    # db session from db_dependency
    db: db_dependency,
    todo_id: int = Path(gt=0),
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found.")


"""
@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(
        db: db_dependency,
        todo_id: int = Path(gt=0)
):
    print("Todo:", todo_id, type(todo_id))
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="todo not found.")
"""


# post a todo
@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(
    user: user_dependency, db: db_dependency, todo_request: TodoRequest
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get("id"))

    db.add(todo_model)
    db.commit()

    return {"message": "todo created", "todo_id": todo_model.id}


"""
@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(
        db: db_dependency,
        todo_request: TodoRequest
):
    todo_model = Todos(**todo_request.dict())

    db.add(todo_model)
    db.commit()
"""


# put request:
# request parameters should be before path param
# @router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
# Update todo by id, with user access token validation
@router.put("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(
    user: user_dependency,
    db: db_dependency,
    todo_request: TodoRequest,
    todo_id: int = Path(gt=0),
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()

    return {"message": "Update completed", "todo_id": todo_model.id}


"""    
@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    db: db_dependency,
    todo_request: TodoRequest,
    todo_id: int = Path(gt=0),
):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()
    # db.refresh(todo_model)

    return {"id": todo_model.id}
"""


# Delete todo by id, by owner_id, with user access_token validation
# @router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
@router.delete("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")
    db.query(Todos).filter(Todos.id == todo_id).filter(
        Todos.owner_id == user.get("id")
    ).delete()

    db.commit()

    return {"message": "delete successfully", "todo_id": todo_model.id}


"""
@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
"""
