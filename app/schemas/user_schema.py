from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas.role_schema import RoleRead


class UserBase(BaseModel):
    full_name: str = Field(..., max_length=100)
    email: EmailStr
    role_id: int
    status: str = "Active"


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100)


class UserUpdate(BaseModel):
    full_name: str | None = Field(None, max_length=100)
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=6, max_length=100)
    role_id: int | None = None
    status: str | None = None


class UserRead(BaseModel):
    user_id: int
    full_name: str
    email: EmailStr
    status: str
    created_at: datetime
    role: RoleRead | None = None

    model_config = ConfigDict(from_attributes=True)


class RegisterRequest(UserCreate):
    pass


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthUserResponse(BaseModel):
    user_id: int
    full_name: str
    email: EmailStr
    role: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: AuthUserResponse


class MeResponse(BaseModel):
    user_id: int
    full_name: str
    email: EmailStr
    role: str
    status: str
