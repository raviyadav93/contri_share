"""Group model."""
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from app.models.base import TimestampMixin


class Group(SQLModel, TimestampMixin, table=True):
    """Group model for expense sharing."""
    
    __tablename__ = "groups"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    created_by: int = Field(foreign_key="users.id")
    currency: str = Field(default="INR")
