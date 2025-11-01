from pydantic import Basemodel

class UserBase(BaseModel):
    username: str
    password: str
    email: str
    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    title: str
    description: str
    completed: bool = False
    class Config:
        orm_mode = True

