from typing import Generator

import pytest
from decouple import config
from fastapi.testclient import TestClient
from tortoise.contrib.test import finalizer, initializer

from app.main import api


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(api) as c:
        yield c


@pytest.fixture(scope="module")
def event_loop(client: TestClient) -> Generator:
    yield client.task.get_loop()


@pytest.fixture(scope="session", autouse=True)
def initialize_tests(request):
    initializer(
        ["app.models.users", "app.models.socials"],
        db_url=config("TORTOISE_TEST_DB", default="sqlite://:memory:"),
    )
    request.addfinalizer(finalizer)
