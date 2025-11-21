from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utils.token import get_current_user
from app.database import get_db
from app import schemas, crud, models



router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


#CREATE
@router.post("",response_model=schemas.TaskCreate,status_code=status.HTTP_201_CREATED)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)

):
    return crud.create_task(db=db, task=task, current_user=current_user)


#READ ALL
@router.get("", response_model=list[schemas.TaskResponse])
def read_tasks(
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    return crud.get_tasks(db=db, current_user=current_user)


#READ ONE BY ID
@router.get('/{task_id}', response_model=schemas.TaskResponse)
def read_one_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_task = crud.get_task_by_id(db=db, task_id=task_id, current_user=current_user)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


#UPDATE
@router.put("/{task_id}", response_model=schemas.TaskUpdate)
def update_task(
    task: schemas.TaskUpdate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.update_task(db=db, task=task, current_user=current_user)


#DELETE
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_task = crud.get_task_by_id(db=db, task_id=task_id, current_user=current_user)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return None


