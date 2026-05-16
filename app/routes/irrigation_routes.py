from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.field import Field
from app.models.irrigation import IrrigationSchedule
from app.models.user import User
from app.schemas.irrigation_schema import IrrigationCreate, IrrigationRead, IrrigationUpdate


router = APIRouter(prefix="/irrigation", tags=["Irrigation"])


@router.get("", response_model=list[IrrigationRead])
def list_irrigation_schedules(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[IrrigationSchedule]:
    return db.query(IrrigationSchedule).order_by(IrrigationSchedule.scheduled_time.asc()).all()


@router.get("/{irrigation_id}", response_model=IrrigationRead)
def get_irrigation_schedule(
    irrigation_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> IrrigationSchedule:
    irrigation = db.get(IrrigationSchedule, irrigation_id)
    if irrigation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Irrigation schedule not found")
    return irrigation


@router.post("", response_model=IrrigationRead, status_code=status.HTTP_201_CREATED)
def create_irrigation_schedule(
    payload: IrrigationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> IrrigationSchedule:
    if db.get(Field, payload.field_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Field not found")

    created_by = payload.created_by or current_user.user_id
    if db.get(User, created_by) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Creator user not found")

    irrigation = IrrigationSchedule(**payload.model_dump(exclude={"created_by"}), created_by=created_by)
    db.add(irrigation)
    db.commit()
    db.refresh(irrigation)
    return irrigation


@router.put("/{irrigation_id}", response_model=IrrigationRead)
def update_irrigation_schedule(
    irrigation_id: int,
    payload: IrrigationUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> IrrigationSchedule:
    irrigation = db.get(IrrigationSchedule, irrigation_id)
    if irrigation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Irrigation schedule not found")

    data = payload.model_dump(exclude_unset=True)
    if "field_id" in data and db.get(Field, data["field_id"]) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Field not found")
    if "created_by" in data and data["created_by"] is not None and db.get(User, data["created_by"]) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Creator user not found")

    for key, value in data.items():
        setattr(irrigation, key, value)

    db.commit()
    db.refresh(irrigation)
    return irrigation


@router.delete("/{irrigation_id}")
def delete_irrigation_schedule(
    irrigation_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict[str, str]:
    irrigation = db.get(IrrigationSchedule, irrigation_id)
    if irrigation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Irrigation schedule not found")

    db.delete(irrigation)
    db.commit()
    return {"message": "Irrigation schedule deleted successfully"}
