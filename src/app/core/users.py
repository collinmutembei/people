from typing import Optional

from beanie import PydanticObjectId
from decouple import config
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import BeanieUserDatabase, ObjectIDIDMixin
from httpx_oauth.clients.google import GoogleOAuth2
from loguru import logger

from app.core.email import (
    ACCOUNT_VERIFICATION_EMAIL_SUBJECT,
    PASSWORD_RESET_EMAIL_SUBJECT,
    EmailSchema,
    sender,
)
from app.db import User, get_user_db

# from app.schemas.users import UserBase, UserCreate, UserDB, UserUpdate

SECRET = config("SECRET", default="7bb9f5050b304ca37d2e60d0e3a9d2bf23e859be")
JWT_LIFETIME_SECONDS = 3600

google_oauth_client = GoogleOAuth2(
    config(
        "GOOGLE_CLIENT_ID",
        default="62960819323-86d5jg9dn8nfg24kt987c0e615gsj129.apps.googleusercontent.com",
    ),
    config("GOOGLE_CLIENT_SECRET", default=""),
)


class UserManager(ObjectIDIDMixin, BaseUserManager[User, PydanticObjectId]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        logger.info(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        await sender(
            email=EmailSchema(
                email=[user.email], body={"username": user.email, "token": token}
            ),
            subject=PASSWORD_RESET_EMAIL_SUBJECT,
            template_name="forgot_password",
        )
        logger.info(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        await sender(
            email=EmailSchema(
                email=[user.email], body={"username": user.email, "token": token}
            ),
            subject=ACCOUNT_VERIFICATION_EMAIL_SUBJECT,
            template_name="verify_token",
        )
        logger.info(
            f"Verification requested for user {user.id}. Verification token: {token}"
        )


async def get_user_manager(user_db: BeanieUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, PydanticObjectId](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
