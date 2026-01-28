from sqlmodel import SQLModel, Field
from typing import Optional, List
from .schemas import TaskBase, UserBase

class Task(TaskBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user_id")

class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    tasks: List["Task"] = []