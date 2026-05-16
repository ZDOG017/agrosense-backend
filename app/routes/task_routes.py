from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.field import Field
from app.models.task import Task
from app.models.user import User
from app.schemas.task_schema import TaskCreate, TaskRead, TaskUpdate


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("", response_model=list[TaskRead])
def list_tasks(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[Task]:
    return db.query(Task).order_by(Task.due_date.asc().nullslast(), Task.task_id.asc()).all()


@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Task:
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Task:
    if payload.assigned_to is not None and db.get(User, payload.assigned_to) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assigned user not found")
    if payload.field_id is not None and db.get(Field, payload.field_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Field not found")

    task = Task(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Task:
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    data = payload.model_dump(exclude_unset=True)
    if "assigned_to" in data and data["assigned_to"] is not None and db.get(User, data["assigned_to"]) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assigned user not found")
    if "field_id" in data and data["field_id"] is not None and db.get(Field, data["field_id"]) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Field not found")

    for key, value in data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict[str, str]:
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}
