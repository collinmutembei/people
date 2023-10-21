from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, File, UploadFile

from app.core.storage import FileStorage, S3FileStorage
from app.core.users import fastapi_users
from app.schemas.contacts import ContactsFileCreate, ContactsFileRead

router = APIRouter()


@router.post("/upload", response_model=Optional[ContactsFileRead])
async def upload_contacts(
    contacts_file: UploadFile = File(...),
    storage_client: FileStorage = Depends(S3FileStorage),
    user=Depends(fastapi_users.current_user(active=True)),
):
    upload = storage_client.upload_file(
        uploader_uuid=user.email, file_upload=contacts_file
    )
    if upload:
        #  TODO: Read CSV file and create users and social accounts
        contact_file_obj = await ContactsFileCreate(
            name=upload.filename, uploader=user
        ).create()
        contact_file_obj.modified_at = datetime.utcnow()  # type: ignore
        await contact_file_obj.insert()
        return contact_file_obj
