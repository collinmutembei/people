import sys
from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastui import AnyComponent, FastUI
from fastui import components as c
from fastui import prebuilt_html
from fastui.components.display import DisplayLookup, DisplayMode
from fastui.events import BackEvent, GoToEvent
from loguru import logger

from api.core.users import (  # current_active_user,
    SECRET,
    auth_backend,
    fastapi_users,
    google_oauth_client,
)
from api.db import ContactsFile, SocialAccount, SocialNetwork, User, db
from api.routes.contacts import router as ContactsUploadRouter
from api.routes.profiles import router as SocialProfileRouter
from api.routes.socials import router as SocialNetworkRouter
from api.schemas.users import UserCreate, UserRead, UserUpdate
from api.settings.openapi import openapi_config

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
            SocialAccount,
            SocialNetwork,
            ContactsFile,
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

api.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=True),
    prefix="/auth/jwt",
    tags=["auth"],
)
api.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
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
    fastapi_users.get_oauth_router(google_oauth_client, auth_backend, SECRET),
    prefix="/auth/google",
    tags=["auth"],
)
api.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

api.include_router(SocialNetworkRouter, prefix="/socialnetwork", tags=["socialnetwork"])
api.include_router(SocialProfileRouter, prefix="/socialprofile", tags=["socialprofile"])
api.include_router(ContactsUploadRouter, prefix="/contacts", tags=["uploads"])


@api.get("/api/", response_model=FastUI, response_model_exclude_none=True)
async def networks_table() -> list[AnyComponent]:
    """
    Show a table of people, `/api` is the endpoint the frontend will connect to
    when a user visits `/` to fetch components to render.
    """
    networks = await SocialNetwork.find_all(fetch_links=True).to_list()
    return [
        c.Page(
            components=[
                c.Heading(text="People", level=2),
                c.Table(
                    data=networks,
                    columns=[
                        DisplayLookup(
                            field="name",
                            on_click=GoToEvent(url="/network/{name}/"),
                        ),
                        DisplayLookup(
                            field="domain",
                        ),
                    ],
                ),
            ]
        ),
    ]


@api.get(
    "/api/network/{network_name}/",
    response_model=FastUI,
    response_model_exclude_none=True,
)
async def social_account(network_name: str) -> list[AnyComponent]:
    """
    User social account page, the frontend will fetch this when the user visits `/network/{name}/`.
    """
    social_accounts = await SocialAccount.find(
        SocialAccount.network.name == network_name, fetch_links=True
    ).to_list()
    return [
        c.Page(
            components=[
                c.Heading(text=network_name, level=2),
                c.Link(components=[c.Text(text="Back")], on_click=BackEvent()),
                c.Table(
                    data=social_accounts,
                    columns=[
                        DisplayLookup(
                            field="username",
                        ),
                        DisplayLookup(field="user", mode=DisplayMode.json),
                    ],
                ),
            ]
        ),
    ]


@api.get("/{path:path}")
async def homepage() -> HTMLResponse:
    return HTMLResponse(prebuilt_html(title="People"))
