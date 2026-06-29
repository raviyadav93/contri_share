"""User schemas."""
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    mobile: str = Field(..., min_length=10, max_length=15)
    full_name: str


class UserCreate(UserBase):
    """User creation schema."""
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """User update schema."""
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    mobile: Optional[str] = None

class User(UserBase):
    """User response schema."""
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class UserResponse(User):
    """User response with timestamps."""
    pass
