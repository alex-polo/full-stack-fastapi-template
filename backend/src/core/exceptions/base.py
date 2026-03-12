class AppBaseError(Exception):
    """Base exception for the application."""

    def __init__(
        self,
        status_code: int,
        message: str,
        error_code: str | None = None,
    ) -> None:
        """Initialize exception."""
        self.status_code = status_code
        self.message = message
        self.error_code = error_code or f"ERR_{status_code}"


class EntityNotFoundError(AppBaseError):
    """Exception for not found entities."""

    def __init__(self, status_code: int, message: str) -> None:
        """Initialize exception."""
        super().__init__(status_code, message, error_code="ERR_ENTITY_NOT_FOUND")
