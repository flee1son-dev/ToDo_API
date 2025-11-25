from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.utils.hashing import hash_password, verify_password
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
    if not user:
        print("Пользователь не найден")
        return None
    if not verify_password(plain_password=password, hashed_password=user.password):
        print("Пароль некорректен")
        return None
    return user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_by_id(id: int, db: Session, current_user: models.User):
    return db.query(models.User).filter(models.User.id == id).first()


def update_user(
        user_id: int,
        user_update: schemas.UserUpdate,
        db: Session,
        current_user: models.User,
):
    if current_user.id != user_id:
        raise HTTPException(status_code=401, detail="You can update only your own account")
    db_user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "password":
            if value:
                value = hash_password(value)
            else:
                continue
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


def create_task(task: schemas.TaskCreate, db: Session, current_user: models.User):
    db_task = models.Task(
        title=task.title,
        description=task.description,
        completed = task.completed,
        owner_id=current_user.id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(
        db: Session,
        current_user: models.User,
        skip: int = 0,
        limit: int = 100
):
    return db.query(models.Task).filter(models.Task.owner_id == current_user.id).offset(skip).limit(limit).all()

def get_task_by_id( task_id: int, db: Session, current_user: models.User):
    return db.query(models.Task).filter(
        models.Task.owner_id == current_user.id,
        models.Task.id == task_id
    ).first()

def update_task(
        task_id: int,
        db: Session,
        task_update: schemas.TaskUpdate,
        current_user: models.User,
):
    db_task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == current_user.id 
        ).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

# def update_task(
#         db: Session,
#         task_id: int,
#         title: str | None,
#         description: str | None,
#         completed: bool | None
# ):
#     db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
#     if not db_task:
#         raise HTTPException(status_code=404, detail="Task not found")
#     update_data = task_update.model_dump(exclude_unset=True)
#     for key, value in update_data.items():
#         setattr(db_task, key, value)
#     db.commit()
#     db.refresh(db_task)
#     return db_task


def delete_task(task_id: int, db: Session, current_user: models.User):
    db_task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == current_user.id
    ).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return None


