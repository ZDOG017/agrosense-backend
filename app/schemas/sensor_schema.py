from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class SensorBase(BaseModel):
    field_id: int
    sensor_type: str = Field(..., max_length=50)
    status: str = "Online"
    installed_date: date | None = None


class SensorCreate(SensorBase):
    pass


class SensorUpdate(BaseModel):
    field_id: int | None = None
    sensor_type: str | None = Field(None, max_length=50)
    status: str | None = None
    installed_date: date | None = None


class SensorRead(SensorBase):
    sensor_id: int

    model_config = ConfigDict(from_attributes=True)
