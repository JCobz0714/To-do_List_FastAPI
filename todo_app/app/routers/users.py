from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import User, Task
from schemas.user import UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("")
async def get_users(session: Session = Depends(get_session)):
    statement = select(User)
    users = session.exec(statement).all()

    return users

@router.get("/{user_id}")
async def get_user(user_id: int, session: Session = Depends(get_session)):
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

@router.put("/{user_id}")
async def update_user(user_id: int, new_user: UserUpdate, session: Session = Depends(get_session)):
    db_user = session.get(User, user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if db_user.username is not None:
        db_user.username = new_user.username

    if db_user.email is not None:
        db_user.email = new_user.email

    if db_user.password is not None:
        db_user.password = new_user.password

    session.commit()
    session.refresh(db_user)

    return db_user

@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.get(User, user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    session.delete(db_user)
    session.commit()