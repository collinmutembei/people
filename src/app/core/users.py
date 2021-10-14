from typing import Optional

from decouple import config
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import TortoiseUserDatabase
from httpx_oauth.clients.github import GitHubOAuth2
from loguru import logger

from app.db import get_user_db
from app.models.users import UserBase, UserCreate, UserDB, UserUpdate

SECRET = config("SECRET", default="7bb9f5050b304ca37d2e60d0e3a9d2bf23e859be")
JWT_LIFETIME_SECONDS = 3600

github_oauth_client = GitHubOAuth2(
    config("CLIENT_ID"),
    config("CLIENT_SECRET"),
)


class UserManager(BaseUserManager[UserCreate, UserDB]):
    user_db_model = UserDB
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: UserDB, request: Optional[Request] = None):
        logger.info(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: UserDB, token: str, request: Optional[Request] = None
    ):
        logger.info(f"User {user.id} has forgot their password. Reset token: {token}")

    async def after_verification_request(
        self, user: UserDB, token: str, request: Optional[Request] = None
    ):
        logger.info(
            f"Verification requested for user {user.id}. Verification token: {token}"
        )


def get_user_manager(user_db: TortoiseUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


jwt_authentication = JWTAuthentication(  # type: ignore
    secret=SECRET, lifetime_seconds=JWT_LIFETIME_SECONDS, tokenUrl="auth/jwt/login"
)

fastapi_users = FastAPIUsers(
    get_user_manager,
    [jwt_authentication],
    UserBase,
    UserCreate,
    UserUpdate,
    UserDB,
)

current_active_user = fastapi_users.current_user(active=True)
