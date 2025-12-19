from .utils.database.connection import Base
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

# User Model
# uvicorn main:app --reload
class Users(Base):
    # For sqlAlchemy to name db table
    __tablename__ = 'users'

    # Define columns using SQLAlchemy 2.0 style:
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    hashed_password: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[str] = mapped_column(String)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    # Relationship to todos
    todos: Mapped[list["Todos"]] = relationship(back_populates="owner")

# Todos Model
class Todos(Base):
    # For sqlAlchemy to name db table
    __tablename__ = 'todos'

    # Define columns using SQLAlchemy 2.0 style:
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    priority: Mapped[int] = mapped_column()
    complete: Mapped[bool] = mapped_column(Boolean, default=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    # Relationship to user
    owner: Mapped["Users"] = relationship(back_populates="todos")
