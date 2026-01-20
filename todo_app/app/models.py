from sqlmodel import SQLModel, Field
from .schemas import TaskBase, UserBase

class Task(TaskBase, table=True):
    id: int = Field(default=None, primary_key=True)

class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)