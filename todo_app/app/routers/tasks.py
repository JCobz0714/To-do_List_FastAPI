from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.database import get_session
from app.models import Task
from schemas.task import TaskCreate

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