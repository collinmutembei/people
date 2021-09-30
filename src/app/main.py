from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.core.users import fastapi_users, jwt_authentication
from app.routes.auth import router as AuthRouter
from app.routes.people import router as PeopleRouter
from app.settings.openapi import openapi_config
from app.settings.orm import orm_config

api = FastAPI(
    title=openapi_config.name,
    version=openapi_config.version,
    description=openapi_config.description,
)

api.include_router(
    fastapi_users.get_auth_router(jwt_authentication), prefix="/auth/jwt", tags=["auth"]
)
api.include_router(AuthRouter, prefix="/auth/jwt", tags=["auth"])
api.include_router(fastapi_users.get_register_router(), prefix="/auth", tags=["auth"])
api.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
api.include_router(
    fastapi_users.get_verify_router(),
    prefix="/auth",
    tags=["auth"],
)
api.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])
api.include_router(PeopleRouter, prefix="/people", tags=["people"])


register_tortoise(api, **orm_config.dict())
