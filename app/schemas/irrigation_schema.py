from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class IrrigationBase(BaseModel):
    field_id: int
    scheduled_time: datetime
    duration_minutes: int
    water_amount_liters: Decimal
    mode: str = "Manual"
    status: str = "Scheduled"
    created_by: int | None = None


class IrrigationCreate(IrrigationBase):
    pass


class IrrigationUpdate(BaseModel):
    field_id: int | None = None
    scheduled_time: datetime | None = None
    duration_minutes: int | None = None
    water_amount_liters: Decimal | None = None
    mode: str | None = None
    status: str | None = None
    created_by: int | None = None


class IrrigationRead(IrrigationBase):
    irrigation_id: int

    model_config = ConfigDict(from_attributes=True)
