"""Group service."""
from app.services.user_service import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlalchemy.exc import IntegrityError

from app.exceptions import MemberAlreadyExistsError, ResourceNotFoundError
from app.models import Group, GroupMember, User
from app.schemas.group import GroupCreate, GroupMemberResponse, GroupUpdate


class GroupService:
    """Group business logic service."""


    @staticmethod
    async def create_group(
        db: AsyncSession,
        group_create: GroupCreate,
        created_by: int
    ) -> Group:
        """Create a new group."""
        group = Group(
            **group_create.model_dump(),
            created_by=created_by
        )
        db.add(group)
        await db.flush()  # Flush to get the group ID before committing
        db.add(GroupMember(group_id=group.id, user_id=created_by))
        await db.commit()
        await db.refresh(group)
        return group

    @staticmethod
    async def get_group_by_id(
        db: AsyncSession,
        group_id: int
    ) -> Group:
        """Get group by ID."""
        result = await db.execute(
            select(Group).where(Group.id == group_id)
        )
        group = result.scalar_one_or_none()
        if not group:
            raise ResourceNotFoundError("Group", group_id)
        return group

    @staticmethod
    async def get_user_groups(
        db: AsyncSession,
        user_id: int
    ) -> list[Group]:
        """Get all groups for a user."""
        result = await db.execute(
            select(Group).join(GroupMember).where(GroupMember.user_id == user_id)
        )
        return result.scalars().all()

    # @staticmethod
    # async def update_group(
    #     db: AsyncSession,
    #     group_id: int,
    #     group_update: GroupUpdate
    # ) -> Group:
    #     """Update group."""
    #     group = await GroupService.get_group_by_id(db, group_id)
        
    #     update_data = group_update.model_dump(exclude_unset=True)
    #     for key, value in update_data.items():
    #         setattr(group, key, value)
        
    #     db.add(group)
    #     await db.commit()
    #     await db.refresh(group)
    #     return group

    @staticmethod
    async def delete_group(
        db: AsyncSession,
        group_id: int
    ) -> None:
        """Delete group."""
        group = await GroupService.get_group_by_id(db, group_id)
        await db.delete(group)
        await db.commit()

    @staticmethod
    async def remove_group_member(
        db: AsyncSession,
        group_id: int,
        user_id: int
    ) -> None:
        """Remove a member from a group."""
        result = await db.execute(
            select(GroupMember).where(
                GroupMember.group_id == group_id,
                GroupMember.user_id == user_id
            )
        )
        membership = result.scalar_one_or_none()
        if not membership:
            raise ResourceNotFoundError("GroupMember", f"group_id={group_id}, user_id={user_id}")
        
        await db.delete(membership)
        await db.commit()

    @staticmethod
    async def add_group_member(
        db: AsyncSession,
        group_id: int,
        user_id: int
    ) -> GroupMember:
        """Add a member to a group."""
        # Check if group exists
        group = await GroupService.get_group_by_id(db, group_id)
        group_model = group.model_dump()

        user  = await UserService.get_user_by_id(db, user_id)  # Check if user exists
        user_model = user.model_dump()
        
        group_member = GroupMember(group_id=group_id, user_id=user_id)
        try:
            db.add(group_member)
            await db.commit()
        except IntegrityError as e:
            await db.rollback()
            raise MemberAlreadyExistsError(user_model["username"], group_model["name"])
        return group_member
    
    @staticmethod
    async def get_group_members(
        db: AsyncSession,
        group_id: int
    ) -> list[GroupMemberResponse]:
        """Get all members of a group."""
        await GroupService.get_group_by_id(db, group_id)  # Ensure group exists

        statement = (
            select(User.username, User.id.label("user_id"), User.email)
            .join(GroupMember, User.id == GroupMember.user_id)
            .where(GroupMember.group_id == group_id)
        )
        result = await db.execute(statement)
        return [GroupMemberResponse.model_validate(row) for row in result.all()]
    
