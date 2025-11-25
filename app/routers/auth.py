from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import get_db
from app.utils.token import create_access_token, get_current_user
from app.utils.hashing import hash_password

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register",response_model=schemas.UserCreate, status_code=status.HTTP_201_CREATED, )
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_pwd = hash_password(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        password= hashed_pwd,
        first_name=user.first_name,
        last_name=user.last_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.Token)
async def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    print(user.username, user.password)
    db_user = crud.authenticate_user(db, username=user.username, password=user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "Bearer"}




