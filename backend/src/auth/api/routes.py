import logging

from fastapi import APIRouter, Response

from src.auth.api.docs import AuthDocsResponses

from ..dependencies import (
    AuthManagerDep,
    CurrentUserDep,
    FormDataDeps,
    RefreshTokenDep,
)
from .schemas import SuccessResponse, UserRead, UserRegister

log = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/login",
    responses=AuthDocsResponses.get_openapi_login_responses_success(),
)
async def login(
    form_data: FormDataDeps,
    auth_manager: AuthManagerDep,
) -> Response:
    """Login user."""
    log.info("Login attempt | email=%r", form_data.username)
    return await auth_manager.login(form_data.username, form_data.password)


@router.post(
    "/logout",
    responses=AuthDocsResponses.get_openapi_logout_responses_success(),
)
async def logout(
    auth_manager: AuthManagerDep,
    current_user: CurrentUserDep,
    response: Response,
) -> SuccessResponse:
    """Logout user."""
    log.info("Logout requested, user_id=%r", current_user.id)
    await auth_manager.logout(response=response)
    return SuccessResponse(message="Logged out")


@router.post("/register")
async def register(
    user_data: UserRegister,
    auth_manager: AuthManagerDep,
) -> Response:
    """Register user."""
    log.info("Registration attempt | email=%r", user_data.email)
    return await auth_manager.register(user_register=user_data)


@router.get("/user/me")
async def user_me(
    current_user: CurrentUserDep,
) -> UserRead:
    """Get current user."""
    log.debug("User profile requested | user_id=%r", current_user.id)
    return current_user


@router.post(
    "/refresh",
    responses=AuthDocsResponses.get_openapi_login_responses_success(),
)
async def refresh(
    token: RefreshTokenDep,
    auth_manager: AuthManagerDep,
) -> Response:
    """Refresh token."""
    log.debug("Token refresh requested")
    return await auth_manager.refresh_token(refresh_token=token)
