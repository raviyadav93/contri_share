"""User model."""
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from app.models.base import TimestampMixin


class User(SQLModel, TimestampMixin, table=True):
    """User model."""
    
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    mobile: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    full_name: str
    is_active: bool = Field(default=True)
