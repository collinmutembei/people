from fastapi import Depends, FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi_health import health
from fastapi_pagination import add_pagination
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession

from .db import get_session
from .routes.profiles import router as ProfilesRouter

api = FastAPI()

api.include_router(ProfilesRouter, prefix="/profile", tags=["profile"])


def is_database_online(db: AsyncSession = Depends(get_session)):
    try:
        db.connection()
        return True
    except exc.OperationalError:
        return False


api.add_api_route("/health", health([is_database_online]), tags=["internal"])

add_pagination(api)


def custom_openapi():
    """Custom openapi"""
    if api.openapi_schema:
        return api.openapi_schema
    openapi_schema = get_openapi(
        title="People",
        version="0.0.1",
        description="know people",
        routes=api.routes,
    )
    openapi_schema["info"]["x-logo"] = {"url": "https://collinmutembei.dev/favicon.ico"}
    api.openapi_schema = openapi_schema
    return api.openapi_schema


api.openapi = custom_openapi  # type: ignore
