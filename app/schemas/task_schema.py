from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskBase(BaseModel):
    assigned_to: int | None = None
    field_id: int | None = None
    task_title: str = Field(..., max_length=150)
    description: str | None = None
    priority: str = "Medium"
    status: str = "Pending"
    due_date: date | None = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    assigned_to: int | None = None
    field_id: int | None = None
    task_title: str | None = Field(None, max_length=150)
    description: str | None = None
    priority: str | None = None
    status: str | None = None
    due_date: date | None = None


class TaskRead(TaskBase):
    task_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
