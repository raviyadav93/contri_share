"""Test configuration and fixtures."""
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

from app.core.database import get_db
from main import app


@pytest.fixture(name="session")
def session_fixture():
    """Create test database session."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create test API client."""
    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override
    
    from fastapi.testclient import TestClient
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
