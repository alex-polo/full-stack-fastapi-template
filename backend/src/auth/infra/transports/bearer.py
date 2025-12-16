from fastapi import Response
from fastapi.responses import JSONResponse

from src.auth.exceptions import TransportLogoutNotSupportedError

from .base import BearerResponse, TransportProtocol


class BearerTransport(TransportProtocol):
    """Bearer transport."""

    def __init__(self) -> None:
        """Initialize the Bearer transport."""

    def make_login_response(self, token: str) -> Response:
        """Return a bearer response."""
        return JSONResponse(
            content=BearerResponse(
                access_token=token,
                token_type="bearer",
            ).model_dump()
        )

    def make_logout_response(self) -> Response:
        """Return a logout response."""
        raise TransportLogoutNotSupportedError()
