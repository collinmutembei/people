from fastapi import Depends, FastAPI
from fastapi_health import health
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session

api = FastAPI()


def is_database_online(session: AsyncSession = Depends(get_session)):
    return session


api.add_api_route("/healthz", health([is_database_online]))
