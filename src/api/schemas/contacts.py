from uuid import UUID

from beanie import Link
from pydantic import BaseModel

from api.db import User


class ContactsFileRead(BaseModel):
    id: UUID
    filename: str
    uploader: Link[User]
