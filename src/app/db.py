from fastapi_users.db import TortoiseUserDatabase

from app.models.users import OAuthAccount, User, UserDB


def get_user_db():
    yield TortoiseUserDatabase(UserDB, User, OAuthAccount)
