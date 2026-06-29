"""Group schemas."""
from typing import Optional

from pydantic import BaseModel, Field


class GroupBase(BaseModel):
    """Base group schema."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=500)
    currency: str = Field(default="INR", max_length=3)


class GroupCreate(GroupBase):
    """Group creation schema."""
    pass


class GroupUpdate(BaseModel):
    """Group update schema."""
    name: Optional[str] = None
    description: Optional[str] = None
    currency: Optional[str] = None


class Group(GroupBase):
    """Group response schema."""
    id: int
    created_by: int

    class Config:
        from_attributes = True


class GroupResponse(Group):
    """Group response with details."""
    pass

class GroupMemberAddRequest(BaseModel):
    user_id: int

class GroupMemberAddResponse(BaseModel):
    user_id: int
    group_id: int

class GroupMemberResponse(BaseModel):
    """Group member schema."""
    user_id: int
    email: str
    username: str

    class Config:
        from_attributes = True
