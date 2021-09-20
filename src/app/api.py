from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi_pagination import add_pagination

from .routes.profile import router as ProfileRouter

api = FastAPI()

api.include_router(ProfileRouter, prefix="/people", tags=["profile"])

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
