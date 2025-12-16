import logging
from typing import TYPE_CHECKING

from fastapi import Response

from src.auth.api.schemas import UserRegister
from src.auth.application.user_service import UserService
from src.auth.domain.entities.user import User
from src.auth.exceptions import InvalidTokenError

from .auth_backend import AuthenticationBackend

if TYPE_CHECKING:
    from src.auth.infra.strategies.base import TokenPayload


log = logging.getLogger(__name__)


class AuthManager:
    """Orchestrates authentication and authorization flows."""

    def __init__(
        self,
        authentication_backend: AuthenticationBackend,
        user_service: UserService,
    ) -> None:
        """Initialize with required dependencies.

        Args:
            authentication_backend: Handles token and session responses.
            user_service: Manages user business logic.
        """
        self._auth_backend = authentication_backend
        self._user_service = user_service

    async def login(self, email: str, password: str) -> Response:
        """Authenticate user and return authentication response.

        Args:
            email: User email.
            password: User password.

        Returns:
            HTTP response containing tokens or cookies.
        """
        try:
            user: User = await self._user_service.authenticate(email, password)
            log.info(
                "User login successful | user_id=%r, email=%r", user.id, email
            )
            return await self._auth_backend.make_authentication_response(
                user=user
            )
        except Exception:
            log.warning("User login failed | email=%r", email)
            raise

    async def logout(self, response: Response) -> None:
        """Clear user session (e.g., delete refresh token).

        Args:
            response: Response object to modify with logout instructions.
        """
        log.info("User logout initiated")
        await self._auth_backend.make_logout_response(response=response)

    async def refresh_token(self, refresh_token: str | None) -> Response:
        """Issue new authentication tokens using a refresh token.

        Args:
            refresh_token: Refresh token string or None.

        Returns:
            HTTP response with new access (and optionally refresh) token(s).
        """
        try:
            payload: TokenPayload = (
                await self._auth_backend.decode_refresh_token(
                    token=refresh_token
                )
            )
            user: User = await self._user_service.get_active_user_by_id(
                user_id=payload.user_id
            )
            log.info("Token refresh successful | user_id=%r", user.id)
            return await self._auth_backend.make_authentication_response(
                user=user
            )
        except Exception:
            log.warning("Token refresh failed")
            raise

    async def current_user(self, token: str | None) -> User:
        """Retrieve active user from access token.

        Args:
            token: JWT access token or None.

        Returns:
            Authenticated and active user.

        Raises:
            InvalidTokenError: If token is missing, invalid, or not an access token.
        """  # noqa: E501
        if not token:
            log.debug("Access token missing")
            raise InvalidTokenError("Not authenticated")

        try:
            payload: TokenPayload = (
                self._auth_backend._jwt_strategy.decode_token(token=token)
            )
            if payload.token_type != "access":
                log.warning(
                    "Invalid token type provided | token_type=%r",
                    payload.token_type,
                )
                raise InvalidTokenError("Not an access token")

            user: User = await self._user_service.get_active_user_by_id(
                payload.user_id
            )
            log.debug("Current user resolved | user_id=%r", user.id)
            return user
        except Exception:
            log.warning("Failed to resolve current user from token")
            raise

    async def register(self, user_register: UserRegister) -> Response:
        """Register a new user and return authentication response.

        Args:
            user_register: User registration data.

        Returns:
            HTTP response with initial authentication tokens or cookies.
        """
        try:
            user: User = await self._user_service.registration(
                user_register=user_register
            )
            log.info(
                "User registration successful | user_id=%r, email=%r",
                user.id,
                user.email,
            )
            return await self._auth_backend.make_authentication_response(
                user=user
            )
        except Exception:
            log.error(
                "User registration failed | email=%r", user_register.email
            )
            raise
