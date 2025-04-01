from datetime import datetime
from uuid import UUID

from pydantic import EmailStr, field_validator

from app.schemas import BaseModel


class UserBase(BaseModel):
    password: str

    @field_validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v


class UserLogin(UserBase):
    username: str

    @field_validator("username")
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters long")
        return v


class UserCreate(UserLogin):
    email: EmailStr
    client_name: str | None
    client_id: UUID | None


class ProfileUpdate(BaseModel):
    avatar_url: str | None
    full_name: str | None


# Output Schemas
class ProfileOut(ProfileUpdate):
    client_id: UUID
    user_id: UUID
    status: str | None
    last_login_at: datetime | None
    created_at: datetime
    updated_at: datetime
