from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import jwt

from src.auth.exceptions import ExpiredTokenError, InvalidTokenError

from .base import BaseJWTStrategy, TokenPayload


class RS256JWTStrategy(BaseJWTStrategy):
    """RS256 JWT strategy."""

    def __init__(
        self,
        private_key_path: str,
        public_key_path: str,
        access_token_expire_minutes: int = 30,
        refresh_token_expire_days: int = 30,
    ) -> None:
        """Initialize the RS256JWTStrategy."""
        self._private_key = Path(private_key_path).read_text(encoding="utf-8")
        self._public_key = Path(public_key_path).read_text(encoding="utf-8")
        self._access_expire = access_token_expire_minutes
        self._refresh_expire = refresh_token_expire_days
        self._algorithm = "RS256"

    def _encode(self, payload: dict[str, Any]) -> str:
        """Encode a payload."""
        return jwt.encode(
            payload, self._private_key, algorithm=self._algorithm
        )  # type: ignore

    def _decode(self, token: str) -> dict[str, Any]:
        """Decode a token."""
        try:
            payload = jwt.decode(
                token, self._public_key, algorithms=[self._algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError as e:
            raise ExpiredTokenError("Token expired") from e
        except jwt.PyJWTError as e:
            raise InvalidTokenError("Invalid token") from e

    def create_access_token(
        self, user_id: int, scopes: list[str] | None = None
    ) -> str:
        """Create an access token."""
        expire: datetime = datetime.now(UTC) + timedelta(
            minutes=self._access_expire
        )
        payload: dict[str, str | datetime | list[str]] = {
            "sub": str(user_id),
            "exp": expire,
            "token_type": "access",
        }
        if scopes:
            payload["scopes"] = scopes
        return self._encode(payload)

    def create_refresh_token(self, user_id: int) -> str:
        """Create a refresh token."""
        expire: datetime = datetime.now(UTC) + timedelta(
            days=self._refresh_expire
        )
        payload: dict[str, str | datetime | list[str]] = {
            "sub": str(user_id),
            "exp": expire,
            "token_type": "refresh",
        }
        return self._encode(payload)

    def decode_token(self, token: str) -> TokenPayload:
        """Decode a token."""
        payload = self._decode(token)
        return TokenPayload(
            user_id=int(payload["sub"]),
            token_type=payload["token_type"],
            scopes=payload.get("scopes"),
        )
