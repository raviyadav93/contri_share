"""Exception handlers."""
from typing import Optional

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from starlette.requests import Request


class AppException(Exception):
    """Base application exception."""
    
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        error_code: Optional[str] = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or "APP_ERROR"


class ResourceNotFoundError(AppException):
    """Resource not found exception."""
    
    def __init__(self, resource: str, resource_id: int):
        super().__init__(
            message=f"{resource} with id {resource_id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="RESOURCE_NOT_FOUND"
        )


class UnauthorizedError(AppException):
    """Unauthorized access exception."""
    
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="UNAUTHORIZED"
        )

class DuplicateResourceError(AppException):
    """Resource already exists exception."""

    def __init__(self, field: str, value: str):
        super().__init__(
            message=f"User with {field} '{value}' already exists",
            status_code=status.HTTP_409_CONFLICT,
            error_code="DUPLICATE_RESOURCE"
        )


class ValidationError(AppException):
    """Validation error exception."""
    
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="VALIDATION_ERROR"   
        )


class MemberAlreadyExistsError(AppException):
    """Member already exists exception."""

    def __init__(self, field: str, value: str):
        super().__init__(
            message=f"Member {field} already existsin group {value}",
            status_code=status.HTTP_409_CONFLICT,
            error_code="MEMBER_ALREADY_EXISTS"
        )

class InvalidExpenseError(AppException):
    """Invalid expense exception."""

    def __init__(self):
        super().__init__(
            message="Invalid expense data",
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="INVALID_EXPENSE"
        )


async def app_exception_handler(request: Request, exc: AppException):
    """Handle application exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "path": str(request.url)
            }
        }
    )
