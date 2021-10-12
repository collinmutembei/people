from typing import Generator

import pytest
from decouple import config
from fastapi.testclient import TestClient
from tortoise.contrib.test import finalizer, initializer

from app.main import api
from app.settings.orm import DB_MODELS


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(api) as c:
        yield c


@pytest.fixture(scope="module")
def event_loop(client: TestClient) -> Generator:
    yield client.task.get_loop()


@pytest.fixture(scope="session", autouse=True)
def initialize_tests(request):
    # skip aerich.models in DB_MODELS
    initializer(
        modules=DB_MODELS[:-1],
        db_url=config("DATABASE_URL", default="sqlite:///tmp/test-{}.sqlite"),
    )
    request.addfinalizer(finalizer)
