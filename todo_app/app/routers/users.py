from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import User, Task
from schemas.user import UserCreate

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/{user_id}")
async def get_users(user_id: int, session: Session = Depends(get_session)):
    db_user = session.get(User, user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return db_user

@router.get("/{user_id}/tasks")
async def get_user_tasks(user_id: int, session: Session = Depends(get_session)):
    user_exist = session.get(User, user_id)

    if not user_exist:
        raise HTTPException(status_code=404, detail="User not found")

    statement = select(Task).where(Task.user_id == user_id)

    tasks = session.exec(statement).all()

    return tasks

@router.post("/create")
async def create_user(user_data: UserCreate, session: Session = Depends(get_session)):
    db_user = User(**user_data.model_dump())

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user