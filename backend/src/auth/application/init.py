import contextlib

import sqlalchemy

from src.auth.application.user_service import UserService
from src.auth.domain.entities.user import User
from src.auth.domain.entities.user_profile import UserProfile
from src.auth.infra.security import hash_password
from src.auth.infra.unitofwork import AuthUnitOfWork
from src.core.config import SERVER_SETTINGS
from src.core.database.db_manager import DB_MANAGER


async def init_admin() -> None:
    """Init admin user."""
    user_session_context = contextlib.asynccontextmanager(
        DB_MANAGER.get_session
    )

    user = User(**SERVER_SETTINGS.ADMIN_USER.model_dump(exclude={"password"}))
    plain_password = SERVER_SETTINGS.ADMIN_USER.password.get_secret_value()
    user.hashed_password = hash_password(plain_password)
    user.profile = UserProfile()

    async with user_session_context() as session:
        try:
            await UserService(uow=AuthUnitOfWork(session)).create_user(
                creation_user=user,
            )
        except sqlalchemy.exc.IntegrityError:  # pyright: ignore[reportAttributeAccessIssue]
            print("User already exists")  # noqa: T201
