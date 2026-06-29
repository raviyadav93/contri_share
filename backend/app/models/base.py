"""Base model for all entities."""
from datetime import datetime

from sqlmodel import Field, SQLModel


class TimestampMixin:
    """Mixin for timestamp fields."""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
