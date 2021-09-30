from datetime import date
from typing import Optional

from fastapi_users import models
from fastapi_users.db import TortoiseBaseUserModel
from tortoise import fields
from tortoise.contrib.pydantic import PydanticModel


class UserBase(models.BaseUser):
    name: str
    birthdate: Optional[date]


class UserCreate(models.BaseUserCreate):
    name: str
    birthdate: Optional[date]


class UserUpdate(models.BaseUserUpdate):
    name: str
    birthdate: Optional[date]


class User(TortoiseBaseUserModel):
    name = fields.CharField(max_length=50)
    birthdate = fields.DateField(null=True)

    def age(self) -> int:
        today = date.today()
        return (
            today.year
            - self.birthdate.year
            - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))
        )

    class PydanticMeta:
        computed = ["age"]


class UserDB(UserBase, models.BaseUserDB, PydanticModel):
    class Config:
        orm_mode = True
        orig_model = User
