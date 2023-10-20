import sys
from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import Depends, FastAPI
from loguru import logger

from app.core.users import (  # SECRET,; github_oauth_client,; linkedin_oauth_client,
    auth_backend,
    current_active_user,
    fastapi_users,
)
from app.db import User, db
from app.schemas.users import UserCreate, UserRead, UserUpdate

# from app.routes.auth import router as AuthRouter
# from app.routes.contacts import router as ContactsUploadRouter
# from app.routes.profiles import router as SocialProfileRouter
# from app.routes.socials import social_network_router as SocialNetworkRouter
from app.settings.openapi import openapi_config

logger.remove()
logger.add(sys.stdout, colorize=True, backtrace=True, diagnose=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
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
    await init_beanie(
        database=db,
        document_models=[
            User,
        ],
    )
    yield


api = FastAPI(
    title=openapi_config.name,
    version=openapi_config.version,
    description=openapi_config.description,
    servers=openapi_config.servers,
    lifespan=lifespan,
)

# api.include_router(fastapi_users.get_register_router(), prefix="/auth", tags=["auth"])
api.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
api.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
# api.include_router(
#     fastapi_users.get_oauth_router(github_oauth_client, SECRET),
#     prefix="/auth/github",
#     tags=["auth"],
# )
# api.include_router(
#     fastapi_users.get_oauth_router(linkedin_oauth_client, SECRET),
#     prefix="/auth/linkedin",
#     tags=["auth"],
# )
api.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
api.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
api.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@api.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


# api.include_router(AuthRouter, prefix="/auth/jwt", tags=["auth"])
# api.include_router(
#     fastapi_users.get_users_router(requires_verification=True),
#     prefix="/users",
#     tags=["users"],
# )
# api.include_router(SocialNetworkRouter)
# api.include_router(SocialProfileRouter, prefix="/socialprofile", tags=["socialprofile"])
# api.include_router(ContactsUploadRouter, prefix="/contacts", tags=["uploads"])
