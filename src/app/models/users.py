from fastapi_users import models
from fastapi_users.db import TortoiseBaseUserModel
from tortoise.contrib.pydantic import PydanticModel


class UserBase(models.BaseUser):
    pass


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(models.BaseUserUpdate):
    pass


class User(TortoiseBaseUserModel):
    pass


class UserDB(UserBase, models.BaseUserDB, PydanticModel):
    class Config:
        orm_mode = True
        orig_model = User
