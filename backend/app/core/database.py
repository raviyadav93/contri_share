"""Database configuration and session management."""
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.core.config import settings

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///"),
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,
)


async def init_db() -> None:
    """Create database tables if they do not exist."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session dependency."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
