from uuid import UUID

from beanie import PydanticObjectId
from pydantic import BaseModel


class ContactsFileRead(BaseModel):
    id: UUID
    name: str
    uploader: PydanticObjectId


class ContactsFileCreate(BaseModel):
    name: str
    uploader: PydanticObjectId
