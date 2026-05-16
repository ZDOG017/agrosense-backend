from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class FieldBase(BaseModel):
    field_name: str = Field(..., max_length=100)
    location: str | None = Field(None, max_length=100)
    area_hectares: Decimal
    soil_type: str | None = Field(None, max_length=50)
    status: str = "Healthy"


class FieldCreate(FieldBase):
    pass


class FieldUpdate(BaseModel):
    field_name: str | None = Field(None, max_length=100)
    location: str | None = Field(None, max_length=100)
    area_hectares: Decimal | None = None
    soil_type: str | None = Field(None, max_length=50)
    status: str | None = None


class FieldRead(FieldBase):
    field_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
