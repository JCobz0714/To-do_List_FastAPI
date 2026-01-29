from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from .schemas import TaskBase, UserBase

class Task(TaskBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="tasks")

class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    tasks: List["Task"] = Relationship(back_populates="user")