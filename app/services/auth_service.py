from sqlalchemy.orm import Session, joinedload

from app.auth import create_access_token, get_password_hash, verify_password
from app.models.role import Role
from app.models.user import User
from app.schemas.user_schema import AuthUserResponse, TokenResponse, UserCreate


def get_user_by_email(db: Session, email: str) -> User | None:
    return (
        db.query(User)
        .options(joinedload(User.role))
        .filter(User.email == email)
        .first()
    )


def create_user(db: Session, user_data: UserCreate) -> User:
    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        role_id=user_data.role_id,
        status=user_data.status,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return (
        db.query(User)
        .options(joinedload(User.role))
        .filter(User.user_id == new_user.user_id)
        .first()
    )


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if user is None or not verify_password(password, user.password_hash):
        return None
    if user.status != "Active":
        return None
    return user


def build_token_response(user: User) -> TokenResponse:
    role_name = user.role.role_name if user.role else ""
    token = create_access_token({"sub": user.email, "role": role_name})
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=AuthUserResponse(
            user_id=user.user_id,
            full_name=user.full_name,
            email=user.email,
            role=role_name,
        ),
    )


def role_exists(db: Session, role_id: int) -> bool:
    return db.query(Role).filter(Role.role_id == role_id).first() is not None
