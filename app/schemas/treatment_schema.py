from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class TreatmentBase(BaseModel):
    field_id: int
    crop_id: int | None = None
    treatment_type: str = Field(..., max_length=50)
    material_used: str | None = Field(None, max_length=100)
    quantity: Decimal | None = None
    unit: str | None = Field(None, max_length=20)
    treatment_date: date | None = None
    cost: Decimal = Decimal("0")
    responsible_user_id: int | None = None


class TreatmentCreate(TreatmentBase):
    pass


class TreatmentUpdate(BaseModel):
    field_id: int | None = None
    crop_id: int | None = None
    treatment_type: str | None = Field(None, max_length=50)
    material_used: str | None = Field(None, max_length=100)
    quantity: Decimal | None = None
    unit: str | None = Field(None, max_length=20)
    treatment_date: date | None = None
    cost: Decimal | None = None
    responsible_user_id: int | None = None


class TreatmentRead(TreatmentBase):
    treatment_id: int

    model_config = ConfigDict(from_attributes=True)
