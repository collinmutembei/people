from datetime import date
from typing import Optional
from uuid import UUID

from fastapi_users import models
from fastapi_users.db import TortoiseBaseUserModel
from pydantic import BaseModel
from tortoise import fields
from tortoise.contrib.pydantic import PydanticModel


class UserBase(models.BaseUser):
    name: str
    birthdate: Optional[date]


class UserCreate(models.BaseUserCreate):
    name: str
    birthdate: Optional[date]


class UserUpdate(models.BaseUserUpdate):
    name: Optional[str]
    birthdate: Optional[date]


class User(TortoiseBaseUserModel):
    name = fields.CharField(max_length=50)
    birthdate = fields.DateField(null=True)

    @property
    def age(self) -> Optional[int]:
        """
        Returns user's age based on birthdate
        Source: https://stackoverflow.com/a/9754466
        """
        today = date.today()
        if self.birthdate:
            return (
                today.year
                - self.birthdate.year
                - (
                    (today.month, today.day)
                    < (self.birthdate.month, self.birthdate.day)
                )
            )
        return None

    class PydanticMeta:
        computed = ["age"]


class UserDB(UserBase, models.BaseUserDB, PydanticModel):
    class Config:
        orm_mode = True
        orig_model = User


class UserBaseModel(BaseModel):
    id: UUID


class UserModel(UserBaseModel):
    name: str
    age: int
