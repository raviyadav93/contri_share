"""User endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse, status_code=201)
async def create_user(
    user_create: UserCreate,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """Create a new user."""
    user = await UserService.create_user(db, user_create)
    return user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """Get user by ID."""
    user = await UserService.get_user_by_id(db, user_id)
    return user


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """Update user."""
    user = await UserService.update_user(db, user_id, user_update)
    return user
