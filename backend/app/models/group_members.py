"""GroupMembers model."""

from sqlmodel import Field, SQLModel

from typing import Optional

from app.models.base import TimestampMixin

class GroupMember(SQLModel, TimestampMixin, table=True):
    """Link table representing the many-to-many relationship between Groups and Users."""
    
    __tablename__ = "group_members"
    
    group_id: int = Field(foreign_key="groups.id", primary_key = True, ondelete="CASCADE")
    user_id: int = Field(foreign_key="users.id", primary_key = True, index=True)
