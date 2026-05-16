from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class HarvestBase(BaseModel):
    crop_id: int
    field_id: int
    harvest_date: date | None = None
    quantity_kg: Decimal
    quality_grade: str | None = None
    price_per_kg: Decimal
    revenue: Decimal | None = None


class HarvestCreate(BaseModel):
    crop_id: int
    field_id: int
    harvest_date: date | None = None
    quantity_kg: Decimal
    quality_grade: str | None = None
    price_per_kg: Decimal


class HarvestUpdate(BaseModel):
    crop_id: int | None = None
    field_id: int | None = None
    harvest_date: date | None = None
    quantity_kg: Decimal | None = None
    quality_grade: str | None = None
    price_per_kg: Decimal | None = None


class HarvestRead(HarvestBase):
    harvest_id: int

    model_config = ConfigDict(from_attributes=True)
