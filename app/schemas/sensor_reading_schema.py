from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class SensorReadingBase(BaseModel):
    sensor_id: int
    reading_value: Decimal
    unit: str = Field(..., max_length=20)
    reading_time: datetime | None = None
    alert_level: str = "Normal"


class SensorReadingCreate(BaseModel):
    sensor_id: int
    reading_value: Decimal
    unit: str = Field(..., max_length=20)
    reading_time: datetime | None = None


class SensorReadingRead(SensorReadingBase):
    reading_id: int

    model_config = ConfigDict(from_attributes=True)
