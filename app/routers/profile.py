from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import get_db
from app.utils.token import create_access_token, get_current_user


router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)

@router.get("", status_code= status.HTTP_200_OK, response_model= schemas.UserResponse)
async def load_profile(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.get_user_by_id(id=current_user.id, db=db, current_user=current_user)



@router.put("/update", response_model= schemas.UserResponse)
async def update_user(
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.update_user(user_id=current_user.id, user_update=user_update, db=db, current_user=current_user)