from typing import Generator

import pytest
from decouple import config
from fastapi.testclient import TestClient
from tortoise.contrib.test import finalizer, initializer

from app.main import api

TEST_DB_URL = config("TEST_DB_URL", default="sqlite://:memory:")


@pytest.fixture(scope="module")
def client() -> Generator:
    initializer(modules=["app.models"], db_url=TEST_DB_URL)
    with TestClient(api) as c:
        yield c
    finalizer()


@pytest.fixture(scope="module")
def event_loop(client: TestClient) -> Generator:
    yield client.task.get_loop()
