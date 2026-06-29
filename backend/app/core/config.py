"""Application configuration."""
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Load .env file from backend directory
env_file = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_file)


class Settings:
    """Application settings."""
    
    PROJECT_NAME: str = "contri_share"
    PROJECT_VERSION: str = "0.1.0"
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./contri_share.db"
    )
    
    # API
    API_V1_STR: str = "/api/v1"
    
    # CORS - Parse comma-separated origins into list
    _CORS_ORIGINS: str = os.getenv(
        "BACKEND_CORS_ORIGINS",
        "http://localhost:5173,http://localhost:3000"
    )
    BACKEND_CORS_ORIGINS: list[str] = [
        origin.strip() for origin in _CORS_ORIGINS.split(",")
    ]
    
    # Security
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "your-secret-key-change-in-production"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Environment
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    

settings = Settings()
