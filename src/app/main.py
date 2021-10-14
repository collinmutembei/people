import sys

from fastapi import FastAPI
from loguru import logger
from tortoise.contrib.fastapi import register_tortoise

from app.core.users import (
    SECRET,
    fastapi_users,
    github_oauth_client,
    jwt_authentication,
)
from app.routes.auth import router as AuthRouter
from app.routes.people import router as PeopleRouter
from app.routes.socials import social_network_router as SocialNetworkRouter
from app.settings.openapi import openapi_config
from app.settings.orm import orm_config

logger.remove()
logger.add(sys.stdout, colorize=True, backtrace=True, diagnose=True)


api = FastAPI(
    title=openapi_config.name,
    version=openapi_config.version,
    description=openapi_config.description,
    servers=openapi_config.servers,
)

api.include_router(fastapi_users.get_register_router(), prefix="/auth", tags=["auth"])
api.include_router(
    fastapi_users.get_auth_router(
        backend=jwt_authentication, requires_verification=True
    ),
    prefix="/auth/jwt",
    tags=["auth"],
)

api.include_router(AuthRouter, prefix="/auth/jwt", tags=["auth"])
api.include_router(
    fastapi_users.get_oauth_router(github_oauth_client, SECRET),
    prefix="/auth/github",
    tags=["auth"],
)

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
api.include_router(
    fastapi_users.get_users_router(requires_verification=True),
    prefix="/users",
    tags=["users"],
)
api.include_router(PeopleRouter, prefix="/people", tags=["people"])
api.include_router(SocialNetworkRouter)

register_tortoise(api, **orm_config.dict())


@api.on_event("startup")
async def log_banner():
    logger.info(
        """

         .8.          8 888888888o    8 8888
        .888.         8 8888    `88.  8 8888
       :88888.        8 8888     `88  8 8888
      . `88888.       8 8888     ,88  8 8888
     .8. `88888.      8 8888.   ,88'  8 8888
    .8`8. `88888.     8 888888888P'   8 8888
   .8' `8. `88888.    8 8888          8 8888
  .8'   `8. `88888.   8 8888          8 8888
 .888888888. `88888.  8 8888          8 8888
.8'       `8. `88888. 8 8888          8 8888

For people
    """
    )
