from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.sensor import Sensor
from app.models.sensor_reading import SensorReading
from app.models.user import User
from app.schemas.sensor_reading_schema import SensorReadingCreate, SensorReadingRead


router = APIRouter(prefix="/sensor-readings", tags=["Sensor Readings"])


@router.get("", response_model=list[SensorReadingRead])
def list_sensor_readings(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[SensorReading]:
    return db.query(SensorReading).order_by(SensorReading.reading_time.desc()).all()


@router.get("/{reading_id}", response_model=SensorReadingRead)
def get_sensor_reading(
    reading_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> SensorReading:
    reading = db.get(SensorReading, reading_id)
    if reading is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor reading not found")
    return reading


@router.post("", response_model=SensorReadingRead, status_code=status.HTTP_201_CREATED)
def create_sensor_reading(
    payload: SensorReadingCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> SensorReading:
    if db.get(Sensor, payload.sensor_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found")

    reading = SensorReading(**payload.model_dump(exclude_none=True))
    db.add(reading)
    db.commit()
    db.refresh(reading)
    return reading


@router.delete("/{reading_id}")
def delete_sensor_reading(
    reading_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict[str, str]:
    reading = db.get(SensorReading, reading_id)
    if reading is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor reading not found")

    db.delete(reading)
    db.commit()
    return {"message": "Sensor reading deleted successfully"}
