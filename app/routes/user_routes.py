from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.auth import get_current_user, get_password_hash, require_roles
from app.database import get_db
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserRead, UserUpdate
from app.services.auth_service import get_user_by_email, role_exists


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=list[UserRead])
def list_users(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[User]:
    return db.query(User).options(joinedload(User.role)).order_by(User.user_id.asc()).all()


@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> User:
    user = db.query(User).options(joinedload(User.role)).filter(User.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post(
    "",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles("Admin", "Farm Manager"))],
)
def create_user_route(payload: UserCreate, db: Session = Depends(get_db)) -> User:
    if get_user_by_email(db, payload.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    if not role_exists(db, payload.role_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    user = User(
        full_name=payload.full_name,
        email=payload.email,
        password_hash=get_password_hash(payload.password),
        role_id=payload.role_id,
        status=payload.status,
    )
    db.add(user)
    db.commit()
    return db.query(User).options(joinedload(User.role)).filter(User.user_id == user.user_id).first()


@router.put(
    "/{user_id}",
    response_model=UserRead,
    dependencies=[Depends(require_roles("Admin", "Farm Manager"))],
)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
) -> User:
    user = db.query(User).options(joinedload(User.role)).filter(User.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    data = payload.model_dump(exclude_unset=True)
    if "email" in data:
        existing_user = get_user_by_email(db, data["email"])
        if existing_user and existing_user.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    if "role_id" in data and not role_exists(db, data["role_id"]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    if "password" in data:
        user.password_hash = get_password_hash(data.pop("password"))

    for key, value in data.items():
        setattr(user, key, value)

    db.commit()
    return db.query(User).options(joinedload(User.role)).filter(User.user_id == user_id).first()


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_roles("Admin"))],
)
def delete_user(user_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
