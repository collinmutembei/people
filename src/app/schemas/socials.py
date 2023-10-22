from typing import Optional
from uuid import UUID

from beanie import Link, PydanticObjectId
from pydantic import BaseModel

from app.db import SocialNetwork, User


class SocialAccountRead(BaseModel):
    id: UUID
    username: str
    network: Link[SocialNetwork]
    user: Link[User]


class SocialAccountCreate(BaseModel):
    username: str
    network_name: str


class SocialAccountUpdate(BaseModel):
    username: str
    network_name: str
    user: PydanticObjectId


class SocialNetworkRead(BaseModel):
    id: UUID
    name: str
    domain: str
    account_prefix: str
    # accounts: Optional[BackLink[SocialAccount]] = []


class SocialNetworkCreate(BaseModel):
    name: str
    domain: str
    account_prefix: Optional[str] = "/"


class SocialNetworkUpdate(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None
    account_prefix: Optional[str] = None
