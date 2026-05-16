from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CropBase(BaseModel):
    field_id: int
    crop_name: str = Field(..., max_length=100)
    planting_date: date
    expected_harvest_date: date | None = None
    growth_stage: str = "Seedling"
    water_requirement_mm: Decimal | None = None
    status: str = "Active"


class CropCreate(CropBase):
    pass


class CropUpdate(BaseModel):
    field_id: int | None = None
    crop_name: str | None = Field(None, max_length=100)
    planting_date: date | None = None
    expected_harvest_date: date | None = None
    growth_stage: str | None = None
    water_requirement_mm: Decimal | None = None
    status: str | None = None


class CropRead(CropBase):
    crop_id: int

    model_config = ConfigDict(from_attributes=True)
