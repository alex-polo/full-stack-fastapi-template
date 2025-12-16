import contextlib
import logging

from sqlalchemy import exc

from src.auth.application.user_service import UserService
from src.auth.domain.entities import User
from src.auth.domain.entities.user_profile import UserProfile
from src.auth.infra.security import hash_password
from src.auth.infra.unitofwork import AuthUnitOfWork
from src.core.config import SERVER_SETTINGS
from src.core.database.db_manager import DB_MANAGER

log = logging.getLogger(__name__)


def initial_user_from_settings() -> User:
    """Create an initial user instance from server settings."""
    log.debug("Creating admin user instance with provided settings")
    user = User(
        **SERVER_SETTINGS.ADMIN_USER.model_dump(
            exclude={"password", "first_name", "patronymic", "last_name"}
        )
    )
    plain_password: str = (
        SERVER_SETTINGS.ADMIN_USER.password.get_secret_value()
    )
    user.hashed_password = hash_password(plain_password)
    user.profile = UserProfile(
        first_name=SERVER_SETTINGS.ADMIN_USER.first_name,
        patronymic=SERVER_SETTINGS.ADMIN_USER.patronymic,
        last_name=SERVER_SETTINGS.ADMIN_USER.last_name,
    )

    return user


async def init_admin() -> None:
    """Initialize the admin user account.

    This function creates an admin user with credentials defined
    in the server settings.

    Raises:
        Exception: Propagates any exceptions from database operations except
                   IntegrityError which indicates user already exists.
    """
    log.info("Initializing admin user")

    db_session_context = contextlib.asynccontextmanager(DB_MANAGER.get_session)

    user: User = initial_user_from_settings()

    log.debug("Admin user instance created with email %r", user.email)

    async with db_session_context() as session:
        try:
            user_service = UserService(uow=AuthUnitOfWork(session))
            log.debug("Find admin user in database")

            user_db: User | None = await user_service.get_user_by_email(
                email=user.email
            )
            if user_db is None:
                log.debug("Attempting to create admin user in database")
                await user_service.create_user(creation_user=user)
                log.info(
                    "Admin user created successfully with email %r",
                    user.email,
                )
            else:
                log.info("Admin user found in database, skipping creation")

        except exc.IntegrityError:
            log.warning(
                "Admin user already exists in database, skipping creation"
            )
