from fastapi import status

from src.auth.infra.transports import BearerResponse

from .schemas import OpenAPIResponseType


class AuthDocsResponses:
    """Auth docs responses."""

    @staticmethod
    def get_openapi_login_responses_success() -> OpenAPIResponseType:
        """Return a dictionary to use for the openapi responses parameter."""
        return {
            status.HTTP_200_OK: {
                "description": "Login successful (auth cookie set)",
                "model": BearerResponse,
                "content": {
                    "application/json": {
                        "example": {
                            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.x",  # noqa: E501
                            "token_type": "bearer",
                        }
                    }
                },
                "headers": {
                    "Set-Cookie": {
                        "schema": {"type": "string"},
                        "description": "Authentication cookie",
                    }
                },
            },
        }

    @staticmethod
    def get_openapi_logout_responses_success() -> OpenAPIResponseType:
        """Return a dictionary to use for the openapi responses parameter."""
        return {
            status.HTTP_200_OK: {
                "description": "Logout successful (auth cookie cleared)",
                "headers": {
                    "Set-Cookie": {
                        "schema": {"type": "string"},
                        "description": "Auth cookie cleared (max-age=0)",
                    }
                },
            }
        }
