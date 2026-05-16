from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.field import Field
from app.models.user import User
from app.schemas.field_schema import FieldCreate, FieldRead, FieldUpdate


router = APIRouter(prefix="/fields", tags=["Fields"])


@router.get("", response_model=list[FieldRead])
def list_fields(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[Field]:
    return db.query(Field).order_by(Field.field_id.asc()).all()


@router.get("/{field_id}", response_model=FieldRead)
def get_field(
    field_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Field:
    field = db.get(Field, field_id)
    if field is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Field not found")
    return field


@router.post("", response_model=FieldRead, status_code=status.HTTP_201_CREATED)
def create_field(
    payload: FieldCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Field:
    field = Field(**payload.model_dump())
    db.add(field)
    db.commit()
    db.refresh(field)
    return field


@router.put("/{field_id}", response_model=FieldRead)
def update_field(
    field_id: int,
    payload: FieldUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Field:
    field = db.get(Field, field_id)
    if field is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Field not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(field, key, value)

    db.commit()
    db.refresh(field)
    return field


@router.delete("/{field_id}")
def delete_field(
    field_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict[str, str]:
    field = db.get(Field, field_id)
    if field is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Field not found")

    db.delete(field)
    db.commit()
    return {"message": "Field deleted successfully"}
