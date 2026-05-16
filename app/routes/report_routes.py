from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.user import User
from app.services.report_service import (
    get_crops_ready_for_harvest,
    get_harvest_revenue_report,
    get_low_moisture_fields,
    get_offline_sensors,
    get_tasks_by_employee,
    get_treatment_costs_by_field,
    get_water_usage_by_field,
)


router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/low-moisture-fields")
def low_moisture_fields(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[dict]:
    return get_low_moisture_fields(db)


@router.get("/water-usage-by-field")
def water_usage_by_field(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[dict]:
    return get_water_usage_by_field(db)


@router.get("/crops-ready-for-harvest")
def crops_ready_for_harvest(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[dict]:
    return get_crops_ready_for_harvest(db)


@router.get("/tasks-by-employee")
def tasks_by_employee(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[dict]:
    return get_tasks_by_employee(db)


@router.get("/offline-sensors")
def offline_sensors(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[dict]:
    return get_offline_sensors(db)


@router.get("/harvest-revenue")
def harvest_revenue(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[dict]:
    return get_harvest_revenue_report(db)


@router.get("/treatment-costs")
def treatment_costs(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[dict]:
    return get_treatment_costs_by_field(db)
