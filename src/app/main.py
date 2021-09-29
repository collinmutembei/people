from fastapi import Depends, FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.core.users import current_active_user, fastapi_users, jwt_authentication
from app.models.users import UserDB
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


@api.get("/authenticated-route")
async def authenticated_route(user: UserDB = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


register_tortoise(api, **orm_config.dict())
