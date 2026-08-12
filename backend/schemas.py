from typing import Optional
from pydantic import BaseModel, Field, field_validator

class UserCreate(BaseModel):
    email: str
    name: str

class UserOut(UserCreate):
    id: int
    model_config = {"from_attributes": True}

class ProjectCreate(BaseModel):
    name: str
    owner_id: int

class ProjectOut(ProjectCreate):
    id: int
    model_config = {"from_attributes": True}

class TaskCreate(BaseModel):
    title: str
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")
    due_date: Optional[str] = None
    status: str = "todo"
    project_id: int

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("title must not be blank")
        return value

class TaskOut(TaskCreate):
    id: int
    model_config = {"from_attributes": True}

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    priority: Optional[str] = Field(default=None, pattern="^(low|medium|high)$")
    due_date: Optional[str] = None
    status: Optional[str] = None
    project_id: Optional[int] = None

    @field_validator("title")
    @classmethod
    def update_title_not_blank(cls, value):
        if value is not None:
            value = value.strip()
            if not value:
                raise ValueError("title must not be blank")
        return value

class QuickAdd(BaseModel):
    description: str
    project_id: int
