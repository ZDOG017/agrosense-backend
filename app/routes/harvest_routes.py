from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.crop import Crop
from app.models.field import Field
from app.models.harvest import HarvestRecord
from app.models.user import User
from app.schemas.harvest_schema import HarvestCreate, HarvestRead, HarvestUpdate


router = APIRouter(prefix="/harvests", tags=["Harvest Records"])


@router.get("", response_model=list[HarvestRead])
def list_harvest_records(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[HarvestRecord]:
    return db.query(HarvestRecord).order_by(HarvestRecord.harvest_date.desc(), HarvestRecord.harvest_id.asc()).all()


@router.get("/{harvest_id}", response_model=HarvestRead)
def get_harvest_record(
    harvest_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> HarvestRecord:
    harvest = db.get(HarvestRecord, harvest_id)
    if harvest is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Harvest record not found")
    return harvest


@router.post("", response_model=HarvestRead, status_code=status.HTTP_201_CREATED)
def create_harvest_record(
    payload: HarvestCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> HarvestRecord:
    if db.get(Crop, payload.crop_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Crop not found")
    if db.get(Field, payload.field_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Field not found")

    harvest = HarvestRecord(**payload.model_dump(exclude_none=True))
    db.add(harvest)
    db.commit()
    db.refresh(harvest)
    return harvest


@router.put("/{harvest_id}", response_model=HarvestRead)
def update_harvest_record(
    harvest_id: int,
    payload: HarvestUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> HarvestRecord:
    harvest = db.get(HarvestRecord, harvest_id)
    if harvest is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Harvest record not found")

    data = payload.model_dump(exclude_unset=True)
    if "crop_id" in data and db.get(Crop, data["crop_id"]) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Crop not found")
    if "field_id" in data and db.get(Field, data["field_id"]) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Field not found")

    for key, value in data.items():
        setattr(harvest, key, value)

    db.commit()
    db.refresh(harvest)
    return harvest


@router.delete("/{harvest_id}")
def delete_harvest_record(
    harvest_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict[str, str]:
    harvest = db.get(HarvestRecord, harvest_id)
    if harvest is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Harvest record not found")

    db.delete(harvest)
    db.commit()
    return {"message": "Harvest record deleted successfully"}
