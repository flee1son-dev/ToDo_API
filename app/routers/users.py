from fastapi import HTTPException, Depends, status, APIRouter
from app import schemas, crud
from app.database import get_db

from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


#READ ALL
@router.get("/", response_model=schemas.UserResponse, status_code=status.HTTP_200_OK)
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


#READ ONE BY ID
@router.get("/{user_id}", response_model=schemas.UserResponse, status_code=status.HTTP_200_OK)
def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


#UPDATE
@router.put("/{user_id}", response_model=schemas.UserUpdate, status_code=status.HTTP_200_OK)
def update_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.update_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


#DELETE
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return None

