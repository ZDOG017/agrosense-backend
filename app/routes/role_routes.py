from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.role import Role
from app.schemas.role_schema import RoleRead


router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("", response_model=list[RoleRead])
def list_roles(
    db: Session = Depends(get_db),
    _: object = Depends(get_current_user),
) -> list[Role]:
    return db.query(Role).order_by(Role.role_id.asc()).all()
