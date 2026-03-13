from typing import TYPE_CHECKING

import pytest
from fastapi.testclient import TestClient

from src.main import app

if TYPE_CHECKING:
    from collections.abc import Generator


@pytest.fixture(scope="module")
def client() -> Generator[TestClient]:
    """Create test client."""
    with TestClient(app) as c:
        yield c
