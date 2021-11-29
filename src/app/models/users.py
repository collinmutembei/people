from datetime import date
from typing import Any, Dict, Optional
from uuid import UUID

from fastapi_users import models
from fastapi_users.db import TortoiseBaseOAuthAccountModel, TortoiseBaseUserModel
from phonenumbers import (
    NumberParseException,
    PhoneNumberFormat,
    PhoneNumberType,
    format_number,
    is_valid_number,
    number_type,
)
from phonenumbers import parse as parse_phone_number
from pydantic import BaseModel, EmailStr, constr, validator
from tortoise import fields
from tortoise.contrib.pydantic import PydanticModel

MOBILE_NUMBER_TYPES = PhoneNumberType.MOBILE, PhoneNumberType.FIXED_LINE_OR_MOBILE


class UserContactInfo(BaseModel):
    email: Optional[EmailStr]
    phone_number: constr(max_length=20, strip_whitespace=True) = None  # type: ignore

    @validator("phone_number")
    def check_phone_number(cls, v):
        if v is None:
            return v

        try:
            n = parse_phone_number(v, "KE")
        except NumberParseException as e:
            raise ValueError("Please provide a valid mobile phone number") from e

        if not is_valid_number(n) or number_type(n) not in MOBILE_NUMBER_TYPES:
            raise ValueError("Please provide a valid mobile phone number")

        return format_number(n, PhoneNumberFormat.INTERNATIONAL)


class UserBase(models.BaseUser, UserContactInfo):  # type: ignore
    name: Optional[str]
    birthdate: Optional[date]
    metadata: Optional[Dict[str, Any]] = {}


class UserCreate(models.BaseUserCreate, UserContactInfo):  # type: ignore
    name: Optional[str]
    birthdate: Optional[date]


class UserUpdate(models.BaseUserUpdate, UserContactInfo):  # type: ignore
    name: Optional[str]
    birthdate: Optional[date]


class User(TortoiseBaseUserModel):
    name = fields.CharField(max_length=50, null=True)
    phone_number = fields.CharField(max_length=20, null=True)
    birthdate = fields.DateField(null=True)
    metadata = fields.JSONField()

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


class UserDB(UserBase, models.BaseUserDB, PydanticModel):  # type: ignore
    class Config:
        orm_mode = True
        orig_model = User


class OAuthAccount(TortoiseBaseOAuthAccountModel):
    user = fields.ForeignKeyField("models.User", related_name="oauth_accounts")


class UserBaseModel(BaseModel):
    id: UUID


class UserModel(UserBaseModel):
    name: str
    age: int
