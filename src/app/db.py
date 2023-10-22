from datetime import date, datetime
from functools import cached_property
from typing import List, Optional
from uuid import UUID, uuid4

import motor.motor_asyncio
from beanie import Document, Indexed, Link
from fastapi_users.db import BaseOAuthAccount, BeanieBaseUser, BeanieUserDatabase
from phonenumbers import (
    NumberParseException,
    PhoneNumberFormat,
    PhoneNumberType,
    format_number,
    is_valid_number,
    number_type,
)
from phonenumbers import parse as parse_phone_number
from pydantic import BaseModel, EmailStr, Field, constr, validator
from pymongo import IndexModel
from pymongo.collation import Collation

from app.settings.base import app_config

DATABASE_NAME = "people"
client = motor.motor_asyncio.AsyncIOMotorClient(
    app_config.db_url, uuidRepresentation="standard"
)
db = client[DATABASE_NAME]

MOBILE_NUMBER_TYPES = PhoneNumberType.MOBILE, PhoneNumberType.FIXED_LINE_OR_MOBILE


class TimestampMixin(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    modified_at: datetime


class AuditActionsMixin(BaseModel):
    created_by: Optional[Link["User"]] = None
    modified_by: Optional[Link["User"]] = None


class OAuthAccount(BaseOAuthAccount):
    pass


class User(BeanieBaseUser, Document):
    email: Optional[EmailStr]
    phone_number: constr(max_length=20, strip_whitespace=True) = None  # type: ignore
    birthdate: Optional[date] = None
    oauth_accounts: List[OAuthAccount] = Field(default_factory=list)

    @cached_property
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

    class Settings:
        name = "users"
        email_collation = Collation("en", strength=2)
        indexes = [
            IndexModel("email", unique=True),
            IndexModel(
                "email", name="case_insensitive_email_index", collation=email_collation
            ),
            IndexModel("phone_number", unique=True),
        ]

    class PydanticMeta:
        computed = ["age"]


class ContactsFile(TimestampMixin, AuditActionsMixin, Document):
    id: UUID = Field(default_factory=uuid4)
    filename: str


class SocialAccount(TimestampMixin, AuditActionsMixin, Document):
    id: UUID = Field(default_factory=uuid4)
    username: Indexed(str)  # type: ignore[valid-type]
    network: Link["SocialNetwork"]
    user: Link[User]

    def __str__(self):
        return f"https://{self.network.domain}{self.network.account_prefix}{self.username}"  # type: ignore

    class Settings:
        name = "social_accounts"


class SocialNetwork(TimestampMixin, AuditActionsMixin, Document):
    id: UUID = Field(default_factory=uuid4)
    name: Indexed(str, unique=True)  # type: ignore[valid-type]
    domain: str
    account_prefix: Optional[str] = "/"
    # accounts: Optional[BackLink[SocialAccount]] = Field(original_field="network")

    class Settings:
        name = "social_networks"


async def get_user_db():
    yield BeanieUserDatabase(User)
