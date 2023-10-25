from typing import Optional

from beanie import PydanticObjectId
from fastapi_users import schemas
from pydantic import EmailStr  # , field_validator

# from api.db import phone_number_validator


class UserRead(schemas.BaseUser[PydanticObjectId]):
    email: Optional[EmailStr] = None
    # phone_number: Optional[str] = None


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    # phone_number: Optional[str] = None

    # _phone_number_validator: classmethod = field_validator("phone_number")(phone_number_validator)


class UserUpdate(schemas.BaseUserUpdate):
    email: Optional[EmailStr] = None
    # phone_number: Optional[str] = None

    # _phone_number_validator: classmethod = field_validator("phone_number")(phone_number_validator)
