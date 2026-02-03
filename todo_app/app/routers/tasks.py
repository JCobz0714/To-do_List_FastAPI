from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import Task, User
from schemas.task import TaskCreate, TaskUpdate

router = APIRouter(prefix="users/{user_id}/tasks", tags=["Tasks"])

@router.get("/")
async def get_tasks(user_id: int, session: Session = Depends(get_session)):
    #Verifying if the user exists
    validate_user_exists(user_id)

    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()
    return tasks

@router.get("/{task_id}")
async def get_task(user_id: int, task_id: int, session: Session = Depends(get_session)):
    validate_user_exists(user_id)

    db_task = session.get(Task, task_id)

    if not db_task or db_task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return db_task;


@router.post("/create/", status_code=201)
async def create_tasks(user_id: int, task_data: TaskCreate, session: Session = Depends(get_session)):
    validate_user_exists(user_id)

    db_task = Task(**task_data.model_dump())

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task

@router.put("/{task_id}")
async def edit_tasks(user_id: int, task_id: int, new_task: TaskUpdate, session: Session = Depends(get_session)):
    validate_user_exists(user_id)

    db_task = session.get(Task, task_id)

    if not db_task or db_task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")

    if new_task.title is not None:
        db_task.title = new_task.title

    if new_task.description is not None:
        db_task.description = new_task.description

    if new_task.completed is not None:
        db_task.completed = new_task.completed
    
    session.commit()
    session.refresh(db_task)

    return db_task

@router.delete("/{task_id}", status_code=204)
async def delete_task(user_id: int, task_id: int, session: Session = Depends(get_session)):
    validate_user_exists(user_id)

    db_task = session.get(Task, task_id)

    if not db_task or db_task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(db_task)
    session.commit()

def validate_user_exists(user_id: int, session: Session):
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")