from typing import Literal

from fastapi import Response, status
from fastapi.security import APIKeyCookie

from .base import TransportProtocol


class CookieTransport(TransportProtocol):
    """Cookie transport."""

    def __init__(
        self,
        cookie_name: str = "auth_token",
        cookie_max_age: int | None = None,
        cookie_path: str = "/",
        cookie_domain: str | None = None,
        cookie_secure: bool = True,
        cookie_httponly: bool = True,
        cookie_samesite: Literal["lax", "strict", "none"] = "lax",
    ):
        """Initialize the Cookie transport."""
        self._cookie_name = cookie_name

        self._cookie_max_age = cookie_max_age
        self._cookie_path = cookie_path
        self._cookie_domain = cookie_domain
        self._cookie_secure = cookie_secure
        self._cookie_httponly = cookie_httponly
        self._cookie_samesite = cookie_samesite
        self.scheme = APIKeyCookie(name=cookie_name, auto_error=False)

    def set_token_in_response(
        self, response: Response, token: str
    ) -> Response:
        """Set auth cookie in response."""
        response.set_cookie(
            key=self._cookie_name,
            value=token,
            max_age=self._cookie_max_age,
            path=self._cookie_path,
            domain=self._cookie_domain,
            secure=self._cookie_secure,
            httponly=self._cookie_httponly,
            samesite=self._cookie_samesite,  # pyright: ignore[reportArgumentType]
        )
        return response

    def make_login_response(self, token: str) -> Response:
        """Set auth cookie and return success response."""
        response = Response(status_code=status.HTTP_200_OK)
        return self.set_token_in_response(response, token)

    def clear_token_in_response(self, response: Response) -> Response:
        """Clear auth cookie in response."""
        response.delete_cookie(
            key=self._cookie_name,
            path=self._cookie_path,
            domain=self._cookie_domain,
            secure=self._cookie_secure,
            httponly=self._cookie_httponly,
            samesite=self._cookie_samesite,  # pyright: ignore[reportArgumentType]
        )
        return response

    def make_logout_response(self) -> Response:
        """Clear auth cookie and return success response."""
        response = Response(status_code=status.HTTP_200_OK)
        return self.clear_token_in_response(response)
