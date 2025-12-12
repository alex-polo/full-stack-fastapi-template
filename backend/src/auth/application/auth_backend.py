import logging

from fastapi import Response

from src.auth.domain.entities.user import User
from src.auth.exceptions import InvalidTokenError
from src.auth.infra.strategies.base import BaseJWTStrategy, TokenPayload
from src.auth.infra.transports.bearer import BearerTransport
from src.auth.infra.transports.cookie import CookieTransport

log = logging.getLogger(__name__)


class AuthenticationBackend:
    """Combines a transport mechanism and JWT strategy to handle authentication flows."""  # noqa: E501

    name: str

    def __init__(
        self,
        name: str,
        jwt_strategy: BaseJWTStrategy,
        bearer_transport: BearerTransport,
        cookie_transport: CookieTransport,
    ) -> None:
        """Initialize the authentication backend.

        Args:
            name: Backend identifier (e.g., 'jwt').
            jwt_strategy: Strategy for encoding/decoding JWT tokens.
            bearer_transport: Handles bearer token responses.
            cookie_transport: Manages refresh tokens in cookies.
        """
        self.name = name
        self._jwt_strategy = jwt_strategy
        self._bearer_transport = bearer_transport
        self._cookie_transport = cookie_transport

    async def make_authentication_response(self, user: User) -> Response:
        """Generate a full authentication response with access and refresh tokens.

        Args:
            user: Authenticated user.

        Returns:
            HTTP response containing access token (in body) and refresh token (in cookie).

        Raises:
            ValueError: If user ID is not set.
        """  # noqa: E501
        if user.id is None:
            raise ValueError("User ID is None")

        access_token: str = self._jwt_strategy.create_access_token(
            user_id=user.id,
            scopes=[],
        )
        refresh_token: str = self._jwt_strategy.create_refresh_token(
            user_id=user.id
        )

        bearer_response = self._bearer_transport.make_login_response(
            access_token
        )

        self._cookie_transport.set_token_in_response(
            response=bearer_response,
            token=refresh_token,
        )

        log.info(
            "Authentication response created | user_id=%r, backend=%r",
            user.id,
            self.name,
        )
        return bearer_response

    async def make_logout_response(self, response: Response) -> None:
        """Clear refresh token from the response cookie.

        Args:
            response: HTTP response to modify.
        """
        self._cookie_transport.clear_token_in_response(response=response)
        log.info("Logout response prepared | backend=%r", self.name)

    async def decode_refresh_token(self, token: str | None) -> TokenPayload:
        """Validate and decode a refresh token.

        Args:
            token: Refresh token string or None.

        Returns:
            Decoded token payload.

        Raises:
            InvalidTokenError: If token is missing, invalid, or not a refresh token.
        """  # noqa: E501
        if not token:
            log.warning("Refresh token missing")
            raise InvalidTokenError("Invalid refresh token")

        try:
            payload: TokenPayload = self._jwt_strategy.decode_token(
                token=token
            )
        except Exception as e:
            log.warning("Failed to decode refresh token")
            raise InvalidTokenError("Invalid refresh token") from e

        if payload.token_type != "refresh":
            log.warning(
                "Invalid token type for refresh operation | token_type=%r",
                payload.token_type,
            )
            raise InvalidTokenError("Not a refresh token")

        log.debug(
            "Refresh token decoded successfully | user_id=%r", payload.user_id
        )
        return payload

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return f"<AuthenticationBackend name={self.name}>"
