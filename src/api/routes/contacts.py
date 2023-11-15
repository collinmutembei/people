from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, File, UploadFile

from api.core.storage import FileStorage, S3FileStorage
from api.core.users import fastapi_users
from api.schemas.contacts import ContactsFileRead
from api.db import ContactsFile

router = APIRouter()


@router.post("/upload", response_model=Optional[ContactsFileRead])
async def upload_contacts(
    contacts_file: UploadFile = File(...),
    storage_client: FileStorage = Depends(S3FileStorage),
    user=Depends(fastapi_users.current_user(active=True)),
):
    upload = storage_client.upload_file(
        uploader_uuid=user.id, file_upload=contacts_file
    )
    if upload:
        #  TODO: Read CSV file and create users and social accounts
        now = datetime.utcnow()
        contact_file_obj = await ContactsFile(
            filename=upload.filename,
            uploader=user,
            created_by=user,
            created_at=now,
            modified_at=now
        ).insert()
        return contact_file_obj
