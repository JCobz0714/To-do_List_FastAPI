from sqlmodel import Field, Session, SQLModel, create_engine, select, table, true

class TaskBase(SQLModel):
    title: str = Field(index=True)
    description: str | None = Field(default=None, index=True)
    completed: bool = Field(default=False)

class UserBase(SQLModel):
    username: str = Field(index=True)
    email: str = Field(index=True)
    password: str = Field(index=True)