from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.crop import Crop
from app.models.field import Field
from app.models.treatment import Treatment
from app.models.user import User
from app.schemas.treatment_schema import TreatmentCreate, TreatmentRead, TreatmentUpdate


router = APIRouter(prefix="/treatments", tags=["Treatments"])


@router.get("", response_model=list[TreatmentRead])
def list_treatments(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[Treatment]:
    return db.query(Treatment).order_by(Treatment.treatment_date.desc(), Treatment.treatment_id.asc()).all()


@router.get("/{treatment_id}", response_model=TreatmentRead)
def get_treatment(
    treatment_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Treatment:
    treatment = db.get(Treatment, treatment_id)
    if treatment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Treatment not found")
    return treatment


@router.post("", response_model=TreatmentRead, status_code=status.HTTP_201_CREATED)
def create_treatment(
    payload: TreatmentCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Treatment:
    if db.get(Field, payload.field_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Field not found")
    if payload.crop_id is not None and db.get(Crop, payload.crop_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Crop not found")
    if payload.responsible_user_id is not None and db.get(User, payload.responsible_user_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Responsible user not found")

    treatment = Treatment(**payload.model_dump(exclude_none=True))
    db.add(treatment)
    db.commit()
    db.refresh(treatment)
    return treatment


@router.put("/{treatment_id}", response_model=TreatmentRead)
def update_treatment(
    treatment_id: int,
    payload: TreatmentUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Treatment:
    treatment = db.get(Treatment, treatment_id)
    if treatment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Treatment not found")

    data = payload.model_dump(exclude_unset=True)
    if "field_id" in data and db.get(Field, data["field_id"]) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Field not found")
    if "crop_id" in data and data["crop_id"] is not None and db.get(Crop, data["crop_id"]) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Crop not found")
    if (
        "responsible_user_id" in data
        and data["responsible_user_id"] is not None
        and db.get(User, data["responsible_user_id"]) is None
    ):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Responsible user not found")

    for key, value in data.items():
        setattr(treatment, key, value)

    db.commit()
    db.refresh(treatment)
    return treatment


@router.delete("/{treatment_id}")
def delete_treatment(
    treatment_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict[str, str]:
    treatment = db.get(Treatment, treatment_id)
    if treatment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Treatment not found")

    db.delete(treatment)
    db.commit()
    return {"message": "Treatment deleted successfully"}
