from uuid import UUID

from beanie import PydanticObjectId
from pydantic import BaseModel


class SocialAccountRead(BaseModel):
    id: UUID
    username: str
    network: PydanticObjectId
    user: PydanticObjectId


class SocialAccountCreate(BaseModel):
    username: str
    network: PydanticObjectId
    user: PydanticObjectId


class SocialAccountUpdate(BaseModel):
    username: str
    user: PydanticObjectId


class SocialNetworkRead(BaseModel):
    id: UUID
    username: str
    network: PydanticObjectId
    user: PydanticObjectId
