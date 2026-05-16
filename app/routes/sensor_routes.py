from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.field import Field
from app.models.sensor import Sensor
from app.models.user import User
from app.schemas.sensor_schema import SensorCreate, SensorRead, SensorUpdate


router = APIRouter(prefix="/sensors", tags=["Sensors"])


@router.get("", response_model=list[SensorRead])
def list_sensors(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[Sensor]:
    return db.query(Sensor).order_by(Sensor.sensor_id.asc()).all()


@router.get("/{sensor_id}", response_model=SensorRead)
def get_sensor(
    sensor_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Sensor:
    sensor = db.get(Sensor, sensor_id)
    if sensor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found")
    return sensor


@router.post("", response_model=SensorRead, status_code=status.HTTP_201_CREATED)
def create_sensor(
    payload: SensorCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Sensor:
    if db.get(Field, payload.field_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Field not found")

    sensor = Sensor(**payload.model_dump(exclude_none=True))
    db.add(sensor)
    db.commit()
    db.refresh(sensor)
    return sensor


@router.put("/{sensor_id}", response_model=SensorRead)
def update_sensor(
    sensor_id: int,
    payload: SensorUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Sensor:
    sensor = db.get(Sensor, sensor_id)
    if sensor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found")

    data = payload.model_dump(exclude_unset=True)
    if "field_id" in data and db.get(Field, data["field_id"]) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Field not found")

    for key, value in data.items():
        setattr(sensor, key, value)

    db.commit()
    db.refresh(sensor)
    return sensor


@router.delete("/{sensor_id}")
def delete_sensor(
    sensor_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> dict[str, str]:
    sensor = db.get(Sensor, sensor_id)
    if sensor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sensor not found")

    db.delete(sensor)
    db.commit()
    return {"message": "Sensor deleted successfully"}
