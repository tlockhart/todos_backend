from typing import Annotated, List, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status

from ..models import Todos
from ..schemas.todo import TodoResponse, TodoRequest
from ..utils.database.connection import get_db_session, get_current_user

# Use APIRouter to define routes
router = APIRouter(prefix="/todos", tags=["todos"])

# We use Any here to prevent Pydantic from trying to generate a schema 
# for the SQLAlchemy Session object during FastAPI's startup inspection.
db_dep = Annotated[Any, Depends(get_db_session)]
user_dep = Annotated[Any, Depends(get_current_user)]

# --- GET ALL TODOS ---
@router.get("/", response_model=List[TodoResponse], status_code=status.HTTP_200_OK)
async def read_all(
    user: user_dep, 
    db: db_dep
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    
    # Cast to Session for IDE autocomplete if needed, 
    # but db is already a Session instance at runtime.
    stmt = select(Todos).where(Todos.owner_id == user.get("id"))
    return db.scalars(stmt).all()


# --- GET SINGLE TODO ---
@router.get("/todo/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
async def read_todo(
    user: user_dep,
    db: db_dep,
    todo_id: Annotated[int, Path(gt=0)]
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todo_model = db.get(Todos, todo_id)
    if todo_model is not None and todo_model.owner_id != user.get("id"):
        todo_model = None
        
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found.")


# --- CREATE TODO ---
@router.post("/todo", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo_request: TodoRequest,
    user: user_dep, 
    db: db_dep
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get("id"))
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model


# --- UPDATE TODO ---
@router.put("/todo/{todo_id}", response_model=None, status_code=status.HTTP_200_OK)
def update_todo(
    todo_request: TodoRequest,
    user: user_dep,
    db: db_dep,
    todo_id: Annotated[int, Path(gt=0)]
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todo_model = db.get(Todos, todo_id)
    if todo_model is not None and todo_model.owner_id != user.get("id"):
        todo_model = None

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()

    return {"message": "Update completed", "todo_id": todo_model.id}


# --- DELETE TODO ---
@router.delete("/todo/{todo_id}", response_model=None, status_code=status.HTTP_200_OK)
async def delete_todo(
    user: user_dep, 
    db: db_dep,
    todo_id: Annotated[int, Path(gt=0)]
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todo_model = db.get(Todos, todo_id)
    if todo_model is not None and todo_model.owner_id != user.get("id"):
        todo_model = None
        
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")
        
    stmt = delete(Todos).where(Todos.id == todo_id, Todos.owner_id == user.get("id"))
    db.execute(stmt)
    db.commit()

    return {"message": "delete successfully", "todo_id": todo_model.id}