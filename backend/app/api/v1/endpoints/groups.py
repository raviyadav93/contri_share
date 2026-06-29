"""Group endpoints."""
from app.services.debt_service import DebtService
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any

from app.core.database import get_db
from app.schemas.group import GroupCreate, GroupMemberAddResponse, GroupMemberResponse, GroupResponse, GroupUpdate, GroupMemberAddRequest
from app.services.group_service import GroupService

router = APIRouter(prefix="/groups", tags=["groups"])


@router.post("", response_model=GroupResponse, status_code=201)
async def create_group(
    group_create: GroupCreate,
    user_id: int = 1,  # TODO: Get from auth token
    db: AsyncSession = Depends(get_db)
) -> GroupResponse:
    """Create a new group."""
    group = await GroupService.create_group(db, group_create, user_id)
    return group

@router.post("/{group_id}/members", response_model=GroupMemberAddResponse, status_code=201)
async def add_group_member(
    group_id: int,
    member_data: GroupMemberAddRequest,
    db: AsyncSession = Depends(get_db)
) -> GroupMemberAddResponse:
    """Add a member to a group."""
    return await GroupService.add_group_member(db, group_id, member_data.user_id)


@router.get("/{group_id}", response_model=GroupResponse)
async def get_group(
    group_id: int,
    db: AsyncSession = Depends(get_db)
) -> GroupResponse:
    """Get group by ID."""
    group = await GroupService.get_group_by_id(db, group_id)
    return group

@router.get("/{group_id}/members", response_model=list[GroupMemberResponse])
async def list_group_members(
    group_id: int,
    db: AsyncSession = Depends(get_db)
) -> list[GroupMemberResponse]:
    """List all members of a group."""
    members = await GroupService.get_group_members(db, group_id)
    return members


@router.get("", response_model=list[GroupResponse])
async def list_user_groups(
    user_id: int = 1,  # TODO: Get from auth token
    db: AsyncSession = Depends(get_db)
) -> list[GroupResponse]:
    """List all groups for a user."""
    groups = await GroupService.get_user_groups(db, user_id)
    return groups


# @router.patch("/{group_id}", response_model=GroupResponse)
# async def update_group(
#     group_id: int,
#     group_update: GroupUpdate,
#     db: AsyncSession = Depends(get_db)
# ) -> GroupResponse:
#     """Update group."""
#     group = await GroupService.update_group(db, group_id, group_update)
#     return group


@router.delete("/{group_id}", status_code=204)
async def delete_group(
    group_id: int,
    db: AsyncSession = Depends(get_db)
) -> None:
    """Delete group."""
    await GroupService.delete_group(db, group_id)

@router.delete("/{group_id}/members/{user_id}", status_code=204)
async def remove_group_member(
    group_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_db)
) -> None:
    """Remove a member from a group."""
    await GroupService.remove_group_member(db, group_id, user_id)

@router.get("/{group_id}/simplify", response_model = Any)
async def simplify_group(
    group_id: int,
    db: AsyncSession = Depends(get_db)
) -> any:
    """Simplify group."""
    simplified_group = await DebtService.simplify_debts(db, group_id)
    return simplified_group