from  fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.staticfiles import StaticFiles

from app.database import engine, SessionLocal, Base
from app.routers import users, auth, tasks


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
app.include_router(auth.router)

Base.metadata.create_all(engine)


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


app.mount("/app", StaticFiles(directory="frontend/dist", html=True), name="frontend")


