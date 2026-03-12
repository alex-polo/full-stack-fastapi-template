from typing import TYPE_CHECKING

from fastapi import status
from fastapi.responses import JSONResponse

from src.core.schemas.error import ErrorDetail, ErrorSchema

if TYPE_CHECKING:
    from fastapi import Request

    from .base import AppBaseError


async def app_error_handler(request: Request, exc: AppBaseError) -> JSONResponse:  # noqa: RUF029
    """Handle AppBaseError exceptions."""
    error_data = ErrorSchema(
        error=ErrorDetail(
            code="ENTITY_NOT_FOUND",
            message=exc.message,
            path=request.url.path,
        )
    )

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=error_data.model_dump(),
    )
