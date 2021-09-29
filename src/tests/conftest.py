from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import api


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(api) as c:
        yield c
