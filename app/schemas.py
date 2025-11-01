from pydantic import BaseModel, Field

class UserBase(BaseModel):
    username: str
    password: str
    email: str


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



