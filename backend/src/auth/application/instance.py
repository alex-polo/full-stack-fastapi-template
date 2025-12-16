from src.auth.infra.strategies.base import BaseJWTStrategy
from src.auth.infra.strategies.rs256 import RS256JWTStrategy
from src.auth.infra.transports.bearer import BearerTransport
from src.auth.infra.transports.cookie import CookieTransport
from src.core.config import SERVER_SETTINGS as SETTINGS

from .auth_backend import AuthenticationBackend

access_token_transport = BearerTransport()

refresh_token_transport = CookieTransport(
    cookie_name=SETTINGS.AUTH.cookie_name,
    cookie_secure=SETTINGS.AUTH.cookie_secure,
    cookie_max_age=SETTINGS.AUTH.cookie_max_age,
    cookie_path=SETTINGS.AUTH.cookie_path,
    cookie_domain=SETTINGS.AUTH.cookie_domain,
    cookie_samesite=SETTINGS.AUTH.cookie_samesite,
    cookie_httponly=True,
)


def get_jwt_strategy() -> BaseJWTStrategy:
    """Return a JWT strategy."""
    return RS256JWTStrategy(
        private_key_path=SETTINGS.AUTH.jwt_private_key_path,
        public_key_path=SETTINGS.AUTH.jwt_public_key_path,
        access_token_expire_minutes=SETTINGS.AUTH.jwt_access_token_expire_minutes,
        refresh_token_expire_days=SETTINGS.AUTH.jwt_refresh_token_expire_days,
    )


authentication_backend = AuthenticationBackend(
    name="jwt",
    jwt_strategy=get_jwt_strategy(),
    bearer_transport=access_token_transport,
    cookie_transport=refresh_token_transport,
)
