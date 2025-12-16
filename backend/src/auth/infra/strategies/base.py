from abc import ABC, abstractmethod

from pydantic import BaseModel


class TokenPayload(BaseModel):
    """Token payload model."""

    user_id: int
    token_type: str
    scopes: list[str] | None = None


class BaseJWTStrategy(ABC):
    """Base JWT strategy."""

    @abstractmethod
    def create_access_token(
        self, user_id: int, scopes: list[str] | None = None
    ) -> str:
        """Create an access token."""
        pass

    @abstractmethod
    def create_refresh_token(self, user_id: int) -> str:
        """Create a refresh token."""
        pass

    @abstractmethod
    def decode_token(self, token: str) -> TokenPayload:
        """Decode a token."""
        pass
