from typing import TYPE_CHECKING

from src.auth.application.exceptions import (
    AccountDisabledError,
    AccountNotVerifiedError,
    InvalidCredentialsError,
    InvalidTokenError,
    NoRolesAssignedError,
)
from src.auth.domain.entities import CookieSettings, TokenEntity
from src.users.domain.entities import UserEntity

if TYPE_CHECKING:
    from src.auth.application.interfaces import ITokenProvider
    from src.core.config.classes import AuthSettings
    from src.core.security.interfaces import IPasswordHasher
    from src.users.application.interfaces import IUserUnitOfWork
    from src.users.domain.entities import UserEntity


class AuthService:
    """Service for managing auth-related business logic."""

    def __init__(
        self,
        uow: IUserUnitOfWork,
        hasher: IPasswordHasher,
        token_provider: ITokenProvider,
        auth_cfg: AuthSettings,
    ) -> None:
        """Initialize AuthService with dependencies."""
        self.uow = uow
        self.hasher = hasher
        self.token_provider = token_provider
        self.auth_cfg = auth_cfg

    def validate_user_status(self, user: UserEntity) -> None:
        """Validate user is active and verified.

        Args:
            user: User entity to validate.

        Raises:
            AccountDisabledError: If user is not active.
            AccountNotVerifiedError: If user is not verified.
        """
        if not user.is_active:
            raise AccountDisabledError()

        if not user.is_verified:
            raise AccountNotVerifiedError()

    def calculate_token_expiration(self) -> int:
        """Calculate token expiration time in seconds.

        Returns:
            Expiration time in seconds from auth settings.
        """
        return (
            self.auth_cfg.cookie_max_age
            if self.auth_cfg.cookie_max_age is not None
            else self.auth_cfg.jwt_refresh_token_expire_days * 24 * 3600
        )

    def create_token_pair(self, access_token: str, refresh_token: str) -> TokenEntity:
        """Create token pair entity with cookie settings.

        Args:
            access_token: JWT access token string.
            refresh_token: JWT refresh token string.

        Returns:
            TokenEntity with tokens and cookie configuration.
        """
        return TokenEntity(
            access_token=access_token,
            refresh_token=refresh_token,
            cookie_settings=CookieSettings(
                name=self.auth_cfg.cookie_name,
                max_age=self.calculate_token_expiration(),
                path=self.auth_cfg.cookie_path,
                domain=self.auth_cfg.cookie_domain,
                secure=self.auth_cfg.cookie_secure,
                samesite=self.auth_cfg.cookie_samesite,
            ),
        )

    def generate_tokens(self, user: UserEntity) -> TokenEntity:
        """Generate access and refresh tokens for user.

        Args:
            user: User entity to generate tokens for.

        Returns:
            TokenEntity containing access and refresh tokens.

        Raises:
            NoRolesAssignedError: If user has no role assignments.
        """
        if not user.roles_assignments:
            raise NoRolesAssignedError()

        self.validate_user_status(user)

        user_roles = [
            a.role.name for a in user.roles_assignments if a.role and a.role.is_active
        ]

        access_token = self.token_provider.create_access_token(
            user_id=user.id,  # type: ignore
            roles=user_roles,
        )
        refresh_token = self.token_provider.create_refresh_token(user_id=user.id)  # type: ignore

        return self.create_token_pair(access_token, refresh_token)

    async def fetch_user_by_id(self, user_id: int) -> UserEntity:
        """Fetch user from database by ID.

        Args:
            user_id: User identifier to fetch.

        Returns:
            UserEntity if found and valid.

        Raises:
            InvalidCredentialsError: If user not found.
            NoRolesAssignedError: If user has no role assignments.
        """
        async with self.uow:
            user: UserEntity | None = await self.uow.users.get_by_id(id=user_id)

            if not user:
                raise InvalidCredentialsError()

            if not user.roles_assignments:
                raise NoRolesAssignedError()

            self.validate_user_status(user=user)

            return user

    async def authenticate(self, username: str, password: str) -> TokenEntity:
        """Authenticate user with credentials and issue tokens.

        Args:
            username: User email or username.
            password: User password in plain text.

        Returns:
            TokenEntity with access and refresh tokens.

        Raises:
            InvalidCredentialsError: If credentials are invalid.
        """
        async with self.uow:
            user = await self.uow.users.get_by_email(email=username)
            if (
                not user
                or not user.id
                or not self.hasher.verify(password, user.hashed_password)
            ):
                raise InvalidCredentialsError()

            return self.generate_tokens(user)

    async def refresh_session(self, refresh_token: str | None) -> TokenEntity:
        """Refresh session using refresh token.

        Args:
            refresh_token: JWT refresh token string.

        Returns:
            TokenEntity with new access and refresh tokens.

        Raises:
            InvalidTokenError: If token is missing or invalid.
            InvalidCredentialsError: If user not found.
        """
        if refresh_token is None:
            raise InvalidTokenError()

        user_payload = self.token_provider.decode_token(refresh_token)
        user_id = user_payload.get("sub")

        if user_payload.get("token_type") != "refresh":
            raise InvalidTokenError()

        if not user_id:
            raise InvalidTokenError()

        user = await self.fetch_user_by_id(user_id=int(user_id))

        return self.generate_tokens(user)

    async def get_current_user(self, jwt_token: str) -> UserEntity:
        """Get authenticated user from JWT access token.

        Args:
            jwt_token: JWT access token string.

        Returns:
            UserEntity of authenticated user.

        Raises:
            InvalidTokenError: If token is invalid or wrong type.
            InvalidCredentialsError: If user not found.
        """
        user_payload = self.token_provider.decode_token(jwt_token)
        user_id = user_payload.get("sub")
        if user_payload.get("token_type") != "access":
            raise InvalidTokenError()

        if not user_id:
            raise InvalidTokenError()

        return await self.fetch_user_by_id(user_id=int(user_id))

    async def logout(self) -> CookieSettings:
        """Create cookie settings for logout (invalidate cookies).

        Returns:
            CookieSettings with max_age=0 to clear auth cookies.
        """
        return CookieSettings(
            name=self.auth_cfg.cookie_name,
            max_age=0,
            path=self.auth_cfg.cookie_path,
            domain=self.auth_cfg.cookie_domain,
            secure=self.auth_cfg.cookie_secure,
            samesite=self.auth_cfg.cookie_samesite,
        )
