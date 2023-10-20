from typing import Optional

import motor.motor_asyncio
from beanie import Document
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase
from phonenumbers import (
    NumberParseException,
    PhoneNumberFormat,
    PhoneNumberType,
    format_number,
    is_valid_number,
    number_type,
)
from phonenumbers import parse as parse_phone_number
from pydantic import EmailStr, constr, validator
from pymongo import IndexModel
from pymongo.collation import Collation

from app.settings.base import app_config

DATABASE_NAME = "people"
client = motor.motor_asyncio.AsyncIOMotorClient(
    app_config.db_url, uuidRepresentation="standard"
)
db = client[DATABASE_NAME]

MOBILE_NUMBER_TYPES = PhoneNumberType.MOBILE, PhoneNumberType.FIXED_LINE_OR_MOBILE


class User(BeanieBaseUser, Document):
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


async def get_user_db():
    yield BeanieUserDatabase(User)
