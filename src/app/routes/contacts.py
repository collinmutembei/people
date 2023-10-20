from datetime import datetime

from fastapi import APIRouter, Depends, File, UploadFile

from app.core.storage import FileStorage, S3FileStorage
from app.core.users import fastapi_users
from app.schemas.contacts import ContactsFile, ContactsFileSchema

router = APIRouter()


@router.post("/upload")
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
        contact_file_obj, _ = await ContactsFile.get_or_create(
            name=upload.filename, uploader_id=user.id
        )
        contact_file_obj.modified_at = datetime.utcnow()  # type: ignore
        await contact_file_obj.save()
    return await ContactsFileSchema.from_tortoise_orm(contact_file_obj)
