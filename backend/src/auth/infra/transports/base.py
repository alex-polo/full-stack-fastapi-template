from typing import Protocol

from fastapi import Response
from pydantic import BaseModel


class BearerResponse(BaseModel):
    """Bearer response model."""

    access_token: str
    token_type: str


class TransportProtocol(Protocol):
    """Base transport protocol."""

    def make_login_response(self, token: str) -> Response:
        """Return a login response."""
        ...

    def make_logout_response(self) -> Response:
        """Return a logout response."""
        ...
