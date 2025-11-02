from pydantic import BaseModel, Field

class UserBase(BaseModel):
    username: str = Field(..., description="User's username")
    password: str = Field(..., description="User's password")
    email: str = Field(..., description="User's email")
    first_name: str = Field(None, description="User's first name")
    last_name: str = Field(None, description="User's last name")


class TaskBase(BaseModel):
    title: str = Field(..., description="Title of the task")
    description: str = Field(None, description="Description of the task")
    completed: bool = Field(default=False, description='Status task')
    owner: UserBase = Field(..., description="Owner of the task")


class UserResponse(UserBase):
    user_id: int

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    email: str | None
    username: str | None
    password: str | None

class UserDelete(UserBase):
    pass


class TaskResponse(TaskBase):
    task_id: int
    user_id: int
    class Config:
        orm_mode = True

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    title: str | None
    description: str | None
    completed: bool

class TaskDelete(TaskBase):
    pass



