from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas
from database import get_db
from .utils.hashing import hash_password, verify_password
from app.utils import token

def create_user(db: Session, username: str, password:str, email: str):
    hashed_pwd = hash_password(password)
    new_user = models.User(username=username, email=email, password= hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not verify_password(password, user.password):
        return None
    return user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = db.query().dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user


def create_task(title: str, current_user: models.User = Depends(token.get_current_user), db: Session = Depends(get_db)):
    db_task = models.Task(title=title, owner_id=current_user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(
        current_user: models.User = Depends(token.get_current_user),
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100
):
    return db.query(models.Task).filter(models.Task.owner_id == current_user.id).offset(skip).limit(limit).all()

def get_task_by_title( task_title: int, db: Session, current_user: models.User = Depends(token.get_current_user)):
    return db.query(models.Task).filter(
        models.Task.owner_id == current_user.id,
        models.Task.title == task_title
    ).first()

def update_task(
        task_id: int,
        title: str,
        db: Session,
        task_update: schemas.TaskUpdate,
        current_user: models.User = Depends(token.get_current_user),
):
    db_task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == current_user.id
        ).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    update_data = task_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(task_id: int, current_user: models.User = Depends(token.get_current_user), db: Session(get_db),):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return db_task


