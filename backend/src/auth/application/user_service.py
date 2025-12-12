import logging

from fastapi import Request

from src.auth.api.schemas import UserRegister
from src.auth.domain.entities.user import User
from src.auth.domain.entities.user_profile import UserProfile
from src.auth.exceptions import InvalidCredentialsError, InvalidTokenError
from src.auth.infra.security import hash_password, verify_password
from src.auth.infra.unitofwork import AuthUnitOfWork

log = logging.getLogger(__name__)


class UserService:
    """Manages user-related business logic including authentication and registration."""  # noqa: E501

    def __init__(self, uow: AuthUnitOfWork) -> None:
        """Initialize the user service with a unit of work.

        Args:
            uow: Unit of work providing access to repositories.
        """
        self.uow = uow

    async def authenticate(self, email: str, password: str) -> User:
        """Authenticate user by email and password.

        Args:
            email: User email.
            password: Plain-text password.

        Returns:
            Authenticated and active user.

        Raises:
            InvalidCredentialsError: If credentials are invalid or user is inactive.
        """  # noqa: E501
        user: User | None = await self.uow.user_repo.get_by_email(email)
        if (
            not user
            or not user.is_active
            or not user.hashed_password
            or not verify_password(
                plain_password=password,
                hashed_password=user.hashed_password,
            )
        ):
            log.warning("Authentication failed | email=%r", email)
            raise InvalidCredentialsError()

        log.info(
            "User authenticated successfully | user_id=%r, email=%r",
            user.id,
            email,
        )
        return user

    async def get_active_user_by_id(self, user_id: int) -> User:
        """Retrieve an active user by ID.

        Args:
            user_id: User identifier.

        Returns:
            Active user.

        Raises:
            InvalidTokenError: If user is not found or inactive.
        """
        user: User | None = await self.uow.user_repo.get_by_id(user_id)

        if not user or not user.is_active:
            log.warning("Active user not found by ID | user_id=%r", user_id)
            raise InvalidTokenError("User inactive or not found")

        log.debug("Active user retrieved | user_id=%r", user_id)
        return user

    async def create_user(self, creation_user: User) -> User:
        """Create a new user.

        Args:
            creation_user: User to create.

        Returns:
            Newly created user.

        Raises:
            Any exception from the repository.
        """
        async with self.uow:
            new_user: User = await self.uow.user_repo.add_user(
                user=creation_user
            )

        log.info(
            "User created successfully | user_id=%r, email=%r",
            new_user.id,
            new_user.email,
        )
        return new_user

    async def registration(self, user_register: UserRegister) -> User:
        """Register a new user.

        Args:
            user_register: Registration data including email, password, and profile.

        Returns:
            Newly created and active user.

        Raises:
            Any exception from the repository.
        """  # noqa: E501
        plain_password = user_register.password.get_secret_value()
        hashed_password = hash_password(plain_password)
        user_entity = User(
            **user_register.model_dump(exclude={"password", "profile"})
        )
        user_entity.hashed_password = hashed_password
        user_entity.is_active = True
        user_entity.is_superuser = False
        user_entity.is_verified = True
        user_entity.profile = UserProfile(**user_register.profile.model_dump())

        user: User = await self.create_user(creation_user=user_entity)

        log.info(
            "User registered successfully | user_id=%r, email=%r",
            user.id,
            user.email,
        )
        await self.on_after_register(user)

        return user

    async def on_after_register(self, user: User) -> None:
        """Perform post-registration actions.

        Args:
            user: Registered user.
        """
        log.debug("Post-registration hook triggered | user_id=%r", user.id)

    async def on_after_forgot_password(
        self,
        user: User,
        token: str,  # noqa: ARG002
        request: Request | None = None,  # noqa: ARG002
    ) -> None:
        """Perform actions after password reset request.

        Args:
            user: User who requested password reset.
            token: Reset token.
            request: Optional HTTP request context.
        """
        log.debug("Password reset requested | user_id=%r", user.id)

    async def on_after_request_verify(
        self,
        user: User,
        token: str,  # noqa: ARG002
        request: Request | None = None,  # noqa: ARG002
    ) -> None:
        """Perform actions after email verification request.

        Args:
            user: User requesting email verification.
            token: Verification token.
            request: Optional HTTP request context.
        """
        log.debug("Email verification requested | user_id=%r", user.id)
