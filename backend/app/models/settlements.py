"""Settlement model."""
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

from app.models.base import TimestampMixin


class Settlements(SQLModel, TimestampMixin, table=True):
    """Settlements model."""
    
    __tablename__ = "settlements"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    group_id: int = Field(foreign_key="groups.id", index=True, ondelete="CASCADE")
    from_user_id: int = Field(foreign_key="users.id")
    to_user_id: int = Field(foreign_key="users.id")
    amount: float = Field(gt=0)