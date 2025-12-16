import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .exceptions import ServerError

log = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    """Register exception handlers."""

    @app.exception_handler(ServerError)
    def entity_server_error_handler(
        request: Request,  # noqa: ARG001
        exc: ServerError,
    ) -> JSONResponse:
        """Handle server errors."""
        log.error("Server exception", exc_info=exc)
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message},
        )

    @app.exception_handler(Exception)
    def unexpected_error_handler(
        request: Request,  # noqa: ARG001
        exc: Exception,
    ) -> JSONResponse:
        """Handle unexpected errors."""
        log.error("Unhandled exception", exc_info=exc)

        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )
