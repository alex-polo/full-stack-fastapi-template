from typing import TYPE_CHECKING

from fastapi.responses import JSONResponse

if TYPE_CHECKING:
    from fastapi import Request

    from .base import AppBaseError


async def app_error_handler(request: Request, exc: AppBaseError) -> JSONResponse:  # noqa: RUF029
    """Handle AppBaseError exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "path": request.url.path,
            }
        },
    )
