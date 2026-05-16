from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.crop import Crop
from app.models.field import Field
from app.models.user import User
from app.schemas.crop_schema import CropCreate, CropRead, CropUpdate


router = APIRouter(prefix="/crops", tags=["Crops"])


@router.get("", response_model=list[CropRead])
def list_crops(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[Crop]:
    return db.query(Crop).order_by(Crop.crop_id.asc()).all()


@router.get("/{crop_id}", response_model=CropRead)
def get_crop(
    crop_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Crop:
    crop = db.get(Crop, crop_id)
    if crop is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Crop not found")
    return crop


@router.post("", response_model=CropRead, status_code=status.HTTP_201_CREATED)
def create_crop(
    payload: CropCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Crop:
    if db.get(Field, payload.field_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Field not found")

    crop = Crop(**payload.model_dump())
    db.add(crop)
    db.commit()
    db.refresh(crop)
    return crop


@router.put("/{crop_id}", response_model=CropRead)
def update_crop(
    crop_id: int,
    payload: CropUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Crop:
    crop = db.get(Crop, crop_id)
    if crop is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Crop not found")

    data = payload.model_dump(exclude_unset=True)
    if "field_id" in data and db.get(Field, data["field_id"]) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Field not found")

    for key, value in data.items():
        setattr(crop, key, value)

    db.commit()
    db.refresh(crop)
    return crop


@router.delete("/{crop_id}")
def delete_crop(
    crop_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict[str, str]:
    crop = db.get(Crop, crop_id)
    if crop is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Crop not found")

    db.delete(crop)
    db.commit()
    return {"message": "Crop deleted successfully"}
