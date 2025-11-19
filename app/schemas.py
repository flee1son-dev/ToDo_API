from pydantic import BaseModel, Field

class UserBase(BaseModel):
    username: str = Field(..., description="User's username")
    email: str = Field(..., description="User's email")
    first_name: str = Field(None, description="User's first name")
    last_name: str = Field(None, description="User's last name")


class UserResponse(UserBase):
    user_id: int

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str = Field(..., description="User's password", min_length=1)
    
    

class UserLogin(BaseModel):
    access_token: str
    


class UserUpdate(BaseModel):
    username: str | None = None
    password: str | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    

class UserLogin(BaseModel):
    username: str = Field(..., description="User's username")
    password: str = Field(..., description="User's password")



class TaskBase(BaseModel):
    title: str = Field(..., description="Title of the task")
    description: str = Field(None, description="Description of the task")
    completed: bool = Field(default=False, description='Status task')
    owner_id: int = Field(..., description="User ID owner's task")


class TaskResponse(TaskBase):
    task_id: int = Field(..., description="Task's ID")
    owner_id: int = Field(..., description="Owner's ID")

    class Config:
        orm_mode = True


class TaskCreate(BaseModel):
    title: str
    description: str | None = None


class TaskUpdate(BaseModel):
    title: str = Field(..., description="Task's title", min_length=1)
    description: str | None = None
    completed: bool | None = None



class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"





