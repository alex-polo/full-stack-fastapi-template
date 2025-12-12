from fastapi import FastAPI, Request
from starlette.responses import JSONResponse


class AuthBaseError(Exception):
    """Base auth exception."""

    def __init__(self, message: str, status_code: int = 400) -> None:
        """Initialize the AuthBaseError."""
        self.message = message
        self.status_code = status_code


class TransportLogoutNotSupportedError(AuthBaseError):
    """Raised when logout is not supported."""

    def __init__(
        self,
        message: str = "Transport logout not supported",
    ) -> None:
        """Initialize the TransportLogoutNotSupportedError."""
        super().__init__(message, 401)


class InvalidCredentialsError(AuthBaseError):
    """Raised when the credentials are invalid."""

    def __init__(self, message: str = "Invalid credentials") -> None:
        """Initialize the InvalidCredentialsError."""
        super().__init__(message, status_code=401)


class ExpiredTokenError(AuthBaseError):
    """Raised when the token is expired."""

    def __init__(self, message: str = "Expired token") -> None:
        """Initialize the ExpiredTokenError."""
        super().__init__(message, 401)


class InvalidTokenError(AuthBaseError):
    """Raised when the token is invalid."""

    def __init__(self, message: str = "Invalid token") -> None:
        """Initialize the InvalidTokenError."""
        super().__init__(message, 401)


class InactiveUserError(AuthBaseError):
    """Raised when the user is inactive."""

    def __init__(self, message: str = "Inactive user") -> None:
        """Initialize the InactiveUserError."""
        super().__init__(message, 403)


def register_auth_exception_handlers(app: FastAPI) -> None:
    """Register auth exception handlers."""

    @app.exception_handler(AuthBaseError)
    async def auth_error_handler(  # noqa: RUF029
        request: Request,  # noqa: ARG001
        exc: AuthBaseError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message},
        )
