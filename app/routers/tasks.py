from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas, crud



router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


#CREATE
@router.post("/",response_model=schemas.TaskCreate,status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)


#READ ALL
@router.get("/", response_model=list[schemas.TaskResponse])
def read_tasks(db: Session = Depends(get_db)):
    return crud.get_tasks(db=db)


#READ ONE BY ID
@router.get('/{task_id}', response_model=schemas.TaskResponse)
def read_one_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task_by_id(db=db, task_id=task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


#UPDATE
@router.put("/{task_id}", response_model=schemas.TaskUpdate)
def update_task(task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    return crud.update_task(db=db, task=task)


#DELETE
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task_by_id(db=db, task_id=task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return None


