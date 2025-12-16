import logging
from unittest.mock import patch

from fastapi.testclient import TestClient

from src.auth.infra.unitofwork import AuthUnitOfWork
from src.core.config import SERVER_SETTINGS as SETTINGS

log = logging.getLogger(__name__)


def test_successful_login(
    autenticated_client: TestClient,
) -> None:
    """Test get access token."""
    assert "Authorization" in autenticated_client.headers, (
        "No Authorization in response."
    )

    # Access token
    access_token = autenticated_client.headers["Authorization"]
    assert isinstance(access_token, str), (
        "Expected a string type for access token"
    )
    assert len(access_token) > 0, "An empty access token was received."
    assert access_token.count(".") == 2, "Invalid access token format."

    # Refresh token
    set_cookie = autenticated_client.cookies
    assert "refresh_token" in set_cookie, "No refresh token in cookie header."
    refresh_token = set_cookie["refresh_token"]

    assert isinstance(refresh_token, str), (
        f"Expected a string type for refresh token, but received: "
        f"{type(refresh_token).__name__}."
    )
    assert len(refresh_token) > 0, "An empty refresh token was received."
    assert refresh_token.count(".") == 2, "Invalid refresh token format."


def test_login_with_invalid_email(
    client: TestClient,
    auth_uow: AuthUnitOfWork,  # noqa: ARG001
) -> None:
    """Test login with invalid email."""
    login_data: dict[str, str] = {
        "username": "invalid@email.com",
        "password": SETTINGS.ADMIN_USER.password.get_secret_value(),
    }
    response = client.post(SETTINGS.AUTH.token_url, data=login_data)
    assert response.status_code == 401, "Login with invalid email should fail."


def test_login_with_invalid_password(
    client: TestClient,
    auth_uow: AuthUnitOfWork,  # noqa: ARG001
) -> None:
    """Test login with invalid password."""
    with patch("src.auth.infra.security.verify_password", return_value=False):
        login_data: dict[str, str] = {
            "username": SETTINGS.ADMIN_USER.email,
            "password": "invalid_password",
        }
        response = client.post(SETTINGS.AUTH.token_url, data=login_data)
        assert response.status_code == 401, (
            "Login with invalid password should fail."
        )


def test_register(
    client: TestClient,
    auth_uow: AuthUnitOfWork,
) -> None:
    """Test register endpoint."""
    register_data = {
        "email": "newuser@example.com",
        "password": "newpassword123!",
        "profile": {
            "first_name": "New",
            "patronymic": "User",
            "last_name": "Account",
        },
    }

    with patch.object(auth_uow.user_repo, "get_by_email", return_value=None):
        response = client.post("/api/v1/auth/register", json=register_data)
        assert response.status_code == 200, (
            f"Register should return 200, received: {response.status_code}"
        )


def test_register_with_existing_user(
    client: TestClient,
    auth_uow: AuthUnitOfWork,  # noqa: ARG001
) -> None:
    """Test register endpoint."""
    register_data = {
        "email": SETTINGS.ADMIN_USER.email,
        "password": SETTINGS.ADMIN_USER.password.get_secret_value(),
        "profile": {
            "first_name": SETTINGS.ADMIN_USER.first_name,
            "patronymic": SETTINGS.ADMIN_USER.patronymic,
            "last_name": SETTINGS.ADMIN_USER.last_name,
        },
    }

    response = client.post("/api/v1/auth/register", json=register_data)
    assert response.status_code == 409, (
        f"Register should return 200, received: {response.status_code}"
    )


def test_user_me(autenticated_client: TestClient) -> None:
    """Test user_me endpoint."""
    response = autenticated_client.get("/api/v1/auth/user/me")
    assert response.status_code == 200, "User me endpoint should return 200"


def test_user_me_with_invalid_token(
    client: TestClient,
) -> None:
    """Test user_me endpoint with invalid token."""
    headers = {"Authorization": f"Bearer {'invalid_token'}"}
    response = client.get("/api/v1/auth/user/me", headers=headers)
    assert response.status_code == 401, "User me endpoint should return 401"


def test_logout(
    autenticated_client: TestClient,
) -> None:
    """Test logout endpoint."""
    response = autenticated_client.post("/api/v1/auth/logout")
    assert response.status_code == 200, "Logout should return 200"


def test_logout_with_invalid_token(
    client: TestClient,
) -> None:
    """Test logout endpoint with invalid token."""
    headers = {"Authorization": f"Bearer {'invalid_token'}"}
    response = client.post("/api/v1/auth/logout", headers=headers)
    assert response.status_code == 401, "Logout should return 401"
