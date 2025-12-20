from pydantic import BaseModel, ConfigDict, Field

"""
Pydantic Validations
"""


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool
    # sqlalchemy will auto increment id

class TodoBase(BaseModel):
    title: str
    description: str | None = None
    priority: int
    complete: bool

class TodoCreate(TodoBase):
    owner_id: int

class TodoResponse(TodoBase):
    id: int
    owner_id: int

    # class Config:
    #     orm_mode = True
    
    # Pydantic v2: allow returning ORM objects (SQLAlchemy) directly
    model_config = ConfigDict(from_attributes=True)