from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ProfileDetails(BaseModel):
    name: str
    bio: Optional[dict] = {"about": "", "interests": []}


class Profile(ProfileDetails):
    id: UUID
    active: bool


class ProfileStatus(BaseModel):
    id: UUID
    active: bool
