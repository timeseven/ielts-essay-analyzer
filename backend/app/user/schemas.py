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
    client_id: UUID | None


class ProfileUpdate(BaseModel):
    avatar_url: str
    full_name: str


# Output Schemas
class ProfileOut(ProfileUpdate):
    id: UUID
    client_id: UUID
    user_id: UUID
    status: str
    last_login_at: datetime
    created_at: datetime
    updated_at: datetime
