"""contri_share API application entry point."""
import logging

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import health, users, groups, expenses
from app.core.config import settings
from app.core.database import init_db
from app.exceptions import AppException, app_exception_handler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
app.add_exception_handler(AppException, app_exception_handler)


@app.on_event("startup")
async def startup_event():
    """Startup event handler."""
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.PROJECT_VERSION}")
    await init_db()


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler."""
    logger.info(f"Shutting down {settings.PROJECT_NAME}")


# API v1 routes
api_v1_router = APIRouter()

api_v1_router.include_router(health.router)
api_v1_router.include_router(users.router)
api_v1_router.include_router(groups.router)
api_v1_router.include_router(expenses.router)

app.include_router(api_v1_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["root"])
async def root() -> dict:
    """Root endpoint."""
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "status": "running",
        "docs": f"{settings.API_V1_STR}/docs"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=settings.DEBUG
    )


@app.get("/", tags=["root"])
async def root() -> dict:
    """Root endpoint."""
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "status": "running",
        "docs": f"{settings.API_V1_STR}/docs"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
