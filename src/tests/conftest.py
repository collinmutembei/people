from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.api import api


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(api) as c:
        yield c
