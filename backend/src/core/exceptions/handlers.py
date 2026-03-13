import logging
from collections.abc import Callable, Coroutine
from typing import TYPE_CHECKING, Any, cast

from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.core.schemas.error import ErrorDetail, ErrorSchema

from .base import AppBaseError

if TYPE_CHECKING:
    from fastapi import Request


log = logging.getLogger(__name__)

type HandlerType = Callable[[Request, Any], Coroutine[Any, Any, JSONResponse]]


def app_error_handler(request: Request, exc: AppBaseError) -> JSONResponse:
    """Handle AppBaseError exceptions."""
    log.error("Application server error: %s", exc, exc_info=exc)

    error_data = ErrorSchema(
        error=ErrorDetail(
            code=exc.error_code,
            message=exc.message,
            path=request.url.path,
            details=exc.to_details(),
        )
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=error_data.model_dump(),
    )


def universal_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle global exceptions."""
    log.error("Unhandled error occurred in request: %s", exc, exc_info=exc)

    error_data = ErrorSchema(
        error=ErrorDetail(
            code="INTERNAL_SERVER_ERROR",
            message="Something went wrong on our side",
            path=request.url.path,
            details=None,
        )
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_data.model_dump(),
    )


def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle RequestValidationError exceptions."""
    log.error("Validation error occurred in request: %s", exc, exc_info=exc)

    validation_details = {
        ".".join(str(loc) for loc in err["loc"]): err["msg"] for err in exc.errors()
    }

    error_data = ErrorSchema(
        error=ErrorDetail(
            code="VALIDATION_ERROR",
            message="Invalid input data",
            path=request.url.path,
            details=validation_details,
        )
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_data.model_dump(),
    )


def sqlalchemy_exception_handler(
    request: Request,
    exc: SQLAlchemyError,
) -> JSONResponse:
    """Handle SQLAlchemy errors."""
    log.error("Database error occurred at %s: %s", request.url.path, exc, exc_info=exc)

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_code = "DATABASE_ERROR"
    message = "An unexpected database error occurred."

    if isinstance(exc, IntegrityError):
        status_code = status.HTTP_400_BAD_REQUEST
        error_code = "INTEGRITY_ERROR"
        message = "Data integrity violation (duplicate entry or constraint violation)."

    error_data = ErrorSchema(
        error=ErrorDetail(
            code=error_code,
            message=message,
            path=request.url.path,
            details=None,
        ),
    )
    return JSONResponse(status_code=status_code, content=error_data.model_dump())


def register_exceptions(app: FastAPI) -> None:
    """Register exception handlers."""
    app.add_exception_handler(
        AppBaseError,
        cast("HandlerType", app_error_handler),
    )
    app.add_exception_handler(
        RequestValidationError,
        cast("HandlerType", validation_exception_handler),
    )
    app.add_exception_handler(
        SQLAlchemyError,
        cast("HandlerType", sqlalchemy_exception_handler),
    )
    app.add_exception_handler(
        Exception,
        cast("HandlerType", universal_exception_handler),
    )


__all__ = ("register_exceptions",)
