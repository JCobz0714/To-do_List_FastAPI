from sqlmodel import Field, Session, SQLModel, create_engine, select, table, true

class Task(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str | None = Field(default=None, index=True)
    completed: bool = Field(default=False)

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    email: str = Field(index=True)
    password: str = Field(index=True)