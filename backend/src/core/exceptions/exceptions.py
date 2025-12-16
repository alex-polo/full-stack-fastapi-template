from fastapi import status


class ServerError(Exception):
    """Base class for server errors."""

    def __init__(self, message: str, status_code: int = 400) -> None:
        """Initialize the AuthBaseError."""
        self.message = message
        self.status_code = status_code


class EntityNotFoundError(ServerError):
    """Entity not found error."""

    def __init__(self, message: str = "Entity not found") -> None:
        """Initialize the EntityNotFoundError."""
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class EntityAlreadyExistsError(ServerError):
    """Entity already exists error."""

    def __init__(self, message: str = "Entity already exists") -> None:
        """Initialize the EntityAlreadyExistsError."""
        super().__init__(message, status.HTTP_409_CONFLICT)


class InvalidRequestError(ServerError):
    """Invalid request error."""

    pass  # → 400


class ServiceUnavailableError(ServerError):
    """Service unavailable error."""

    pass  # → 503
