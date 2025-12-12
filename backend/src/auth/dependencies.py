import logging
from collections.abc import AsyncGenerator
from typing import TYPE_CHECKING, Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.security.api_key import APIKeyCookie

from src.auth.application import AuthManager, UserService
from src.core.config import SERVER_SETTINGS as SETTINGS
from src.core.database.db_manager import DBSessionDep

from .api.schemas import UserRead
from .application.instance import authentication_backend
from .infra.unitofwork import AuthUnitOfWork

if TYPE_CHECKING:
    from src.auth.domain.entities.user import User

log = logging.getLogger(__name__)

scheme_oauth2 = OAuth2PasswordBearer(
    tokenUrl=SETTINGS.AUTH.token_url,
    auto_error=False,
)

scheme_cookie = APIKeyCookie(
    name=SETTINGS.AUTH.cookie_name,
    auto_error=False,
)

AccessTokenDep = Annotated[str | None, Depends(scheme_oauth2)]
RefreshTokenDep = Annotated[str | None, Depends(scheme_cookie)]

FormDataDeps = Annotated[
    OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)
]


async def get_auth_uow(  # noqa: RUF029
    session: DBSessionDep,
) -> AsyncGenerator[AuthUnitOfWork]:
    """Get auth uow."""
    yield AuthUnitOfWork(session)


AuthUOWDep = Annotated[AuthUnitOfWork, Depends(get_auth_uow)]


async def get_user_service(  # noqa: RUF029
    uow: AuthUOWDep,
) -> AsyncGenerator[UserService]:
    """Get user manager."""
    yield UserService(uow=uow)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


async def get_auth_manager(  # noqa: RUF029
    user_service: UserServiceDep,
) -> AsyncGenerator[AuthManager]:
    """Get auth manager."""
    yield AuthManager(
        authentication_backend=authentication_backend,
        user_service=user_service,
    )


AuthManagerDep = Annotated[AuthManager, Depends(get_auth_manager)]


async def get_current_user(
    token: AccessTokenDep,
    auth_manager: AuthManagerDep,
) -> UserRead:
    """Get current user db model."""
    if not token:
        log.debug("Access token missing in request")
    try:
        user: User = await auth_manager.current_user(token)
        log.debug("Current user resolved | user_id=%r", user.id)
        return UserRead.model_validate(user)
    except Exception:
        log.debug("Failed to resolve current user from token")
        raise


CurrentUserDep = Annotated[UserRead, Depends(get_current_user)]


__all__ = [
    "AccessTokenDep",
    "AuthManagerDep",
    "AuthUOWDep",
    "CurrentUserDep",
    "FormDataDeps",
    "RefreshTokenDep",
    "UserServiceDep",
]
