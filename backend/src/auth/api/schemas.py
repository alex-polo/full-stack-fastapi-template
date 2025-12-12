from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr, Field, SecretStr

OpenAPIResponseType = dict[int | str, dict[str, Any]]


class SuccessResponse(BaseModel):
    """Success response model."""

    success: bool = True
    message: str


class UserProfileRead(BaseModel):
    """User profile model."""

    user_id: int
    first_name: str | None
    patronymic: str | None
    last_name: str | None
    bio: str | None
    avatar_url: str | None
    timezone: str | None
    locale: str | None
    created_at: datetime
    updated_at: datetime


class UserProfileCreate(BaseModel):
    """User profile create model."""

    first_name: str | None = None
    patronymic: str | None = None
    last_name: str | None = None
    bio: str | None = None
    avatar_url: str | None = None
    timezone: str | None = None
    locale: str | None = None


class UserProfileUpdate(UserProfileCreate):
    """User profile update model."""


class UserRead(BaseModel):
    """User read model."""

    id: int
    email: str
    is_active: bool
    is_superuser: bool
    is_verified: bool
    profile: UserProfileRead | None = None


class UserCreate(BaseModel):
    """User create model."""

    email: EmailStr
    hashed_password: str
    profile: UserProfileCreate | None = None
    is_active: bool | None = False
    is_superuser: bool | None = False
    is_verified: bool | None = False


class UserUpdate(UserCreate):
    """User update model."""


class UserLogin(BaseModel):
    """User login model."""

    email: str
    password: str


class UserRegister(BaseModel):
    """User register model."""

    email: EmailStr
    password: SecretStr = Field(min_length=8)
    profile: UserProfileCreate
