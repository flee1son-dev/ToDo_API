from  fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from models import User, Task
from database import engine, SessionLocal
from crud import *
from routers import *

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(tasks.router)

Base.metadata.create_all(engine)


@app.get("/")
def read_root():
    return {
        "message": "To-Do-API running",
        "endpoint": {
            "users": "/users",
            "tasks": "/tasks",
        }
    }