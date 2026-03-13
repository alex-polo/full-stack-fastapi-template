"""Tests for API endpoints."""

from typing import TYPE_CHECKING

from fastapi import status

if TYPE_CHECKING:
    from fastapi.testclient import TestClient
    from httpx import Response


def test_health_check(client: TestClient) -> None:
    """Test health check endpoint."""
    response: Response = client.get("/api/v1/utils/health-check")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "healthy"}
