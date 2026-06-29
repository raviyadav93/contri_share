"""User service."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlmodel import select as sqlmodel_select

from app.core.security import get_password_hash, verify_password
from sqlalchemy.exc import IntegrityError

from app.core.security import get_password_hash, verify_password
from app.exceptions import ResourceNotFoundError, DuplicateResourceError
from app.models import User
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """User business logic service."""

    @staticmethod
    async def create_user(
        db: AsyncSession,
        user_create: UserCreate
    ) -> User:
        """Create a new user."""
        hashed_password = get_password_hash(user_create.password)
        user = User(
            email=user_create.email,
            username=user_create.username,
            full_name=user_create.full_name,
            mobile=user_create.mobile,
            hashed_password=hashed_password
        )
        db.add(user)
        try:
            await db.commit()
        except IntegrityError as e:
            await db.rollback()
            # Check which field caused the constraint violation
            error_info = str(e.orig).lower()
            if "email" in error_info:
                raise DuplicateResourceError("email", user_create.email)
            elif "mobile" in error_info:
                raise DuplicateResourceError("mobile", user_create.mobile)
            elif "username" in error_info:
                raise DuplicateResourceError("username", user_create.username)
            else:
                raise DuplicateResourceError("email/mobile/username", user_create.email)
        
        await db.refresh(user)
        return user

    @staticmethod
    async def get_user_by_id(
        db: AsyncSession,
        user_id: int
    ) -> User:
        """Get user by ID."""
        result = await db.execute(
            sqlmodel_select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise ResourceNotFoundError("User", user_id)
        return user

    @staticmethod
    async def get_user_by_email(
        db: AsyncSession,
        email: str
    ) -> User | None:
        """Get user by email."""
        result = await db.execute(
            sqlmodel_select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def update_user(
        db: AsyncSession,
        user_id: int,
        user_update: UserUpdate
    ) -> User:
        """Update user."""
        user = await UserService.get_user_by_id(db, user_id)
        
        update_data = user_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)
        
        db.add(user)
        try:
            await db.commit()
        except IntegrityError as e:
            await db.rollback()
            # Check which field caused the constraint violation
            error_info = str(e.orig).lower()
            if "email" in error_info:
                raise DuplicateResourceError("email", user_update.email)
            elif "mobile" in error_info:
                raise DuplicateResourceError("mobile", user_update.mobile)
            elif "username" in error_info:
                raise DuplicateResourceError("username", user_update.username)
            else:
                raise DuplicateResourceError("email/mobile/username", user_update.email)
        await db.refresh(user)
        return user
