from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import create_db_and_tables
from app import models

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)