from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import Task
from schemas.task import TaskCreate, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/")
async def get_tasks(session: Session = Depends(get_session)):
    statement = select(Task)
    tasks = session.exec(statement).all()
    return tasks

@router.post("/create/", status_code=201)
async def create_tasks(task_data: TaskCreate, session: Session = Depends(get_session)):
    db_task = Task(**task_data.model_dump())

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task

@router.put("/{task_id}")
async def edit_tasks(task_id: int, new_task: TaskUpdate, session: Session = Depends(get_session)):
    db_task = session.get(Task, task_id)

    if not db_task:
        raise HTTPException(status_code=404, detail="User not found")

    if new_task.title is not None:
        db_task.title = new_task.title

    if new_task.description is not None:
        db_task.description = new_task.description

    if new_task.completed is not None:
        db_task.completed = new_task.completed
    
    session.commit()
    session.refresh(db_task)

    return db_task