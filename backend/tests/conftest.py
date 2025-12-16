import logging
from collections.abc import Generator
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from src.auth.dependencies import get_auth_uow
from src.auth.domain.entities.user import User
from src.auth.domain.entities.user_profile import UserProfile
from src.auth.infra.security import hash_password
from src.auth.infra.unitofwork import AuthUnitOfWork
from src.core.config import SERVER_SETTINGS as SETTINGS
from src.core.utils import utcnow
from src.main import app
from src.main import app as fastapi_app

log = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def logging_config() -> None:
    """Configure logging for tests."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


@pytest.fixture(scope="module")
def client() -> Generator[TestClient]:
    """Test client fixture."""
    with TestClient(app=fastapi_app) as client:
        yield client


@pytest.fixture(scope="module")
def admin_user_mock() -> User:
    """Admin user fixture."""
    log.debug("Creating admin user instance with provided settings")

    return User(
        id=1,
        email=SETTINGS.ADMIN_USER.email,
        hashed_password=hash_password(
            SETTINGS.ADMIN_USER.password.get_secret_value()
        ),
        is_active=True,
        is_superuser=True,
        is_verified=True,
        profile=UserProfile(
            user_id=1,
            first_name=SETTINGS.ADMIN_USER.first_name,
            patronymic=SETTINGS.ADMIN_USER.patronymic,
            last_name=SETTINGS.ADMIN_USER.last_name,
            bio=None,
            avatar_url=None,
            timezone=None,
            locale=None,
            created_at=utcnow(),
            updated_at=utcnow(),
        ),
        created_at=utcnow(),
        updated_at=utcnow(),
    )


@pytest.fixture(scope="module")
def auth_uow(admin_user_mock: User) -> Generator[AsyncMock]:
    """Create AuthUnitOfWork instance."""
    uow_mock = AsyncMock()
    user_repo_mock = AsyncMock()

    def mock_get_by_email(email: str) -> User | None:
        if email == admin_user_mock.email:
            return admin_user_mock
        return None

    def mock_get_by_id(user_id: int) -> User | None:
        if user_id == admin_user_mock.id:
            return admin_user_mock
        return None

    user_repo_mock.get_by_email.side_effect = mock_get_by_email
    user_repo_mock.get_by_id.side_effect = mock_get_by_id
    uow_mock.user_repo = user_repo_mock

    app.dependency_overrides[get_auth_uow] = lambda: uow_mock

    yield uow_mock

    if get_auth_uow in app.dependency_overrides:
        del app.dependency_overrides[get_auth_uow]


@pytest.fixture(scope="module")
def autenticated_client(
    client: TestClient,
    auth_uow: AuthUnitOfWork,  # noqa: ARG001
) -> Generator[TestClient]:
    """Test client fixture."""
    login_data: dict[str, str] = {
        "username": SETTINGS.ADMIN_USER.email,
        "password": SETTINGS.ADMIN_USER.password.get_secret_value(),
    }
    response = client.post(SETTINGS.AUTH.token_url, data=login_data)
    assert response.status_code == 200, "Login should return 200"

    access_token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    client.headers.update(headers)

    yield client
