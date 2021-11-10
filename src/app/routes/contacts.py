from fastapi import APIRouter, Depends, File, UploadFile

from app.core.storage import FileStorage, S3FileStorage
from app.core.users import fastapi_users
from app.models.contacts import ContactsFile, ContactsFileSchema

router = APIRouter()


@router.post("/upload")
async def upload_contacts(
    contacts_file: UploadFile = File(...),
    storage_client: FileStorage = Depends(S3FileStorage),
    user=Depends(fastapi_users.current_user(active=True)),
):
    # TODO: Read CSV file and create users and social accounts
    uploaded_file = storage_client.upload_file(
        uploader_uuid=user.id, file_upload=contacts_file
    )
    contact_file_obj = await ContactsFile.create(
        name=uploaded_file.object_name, uploader_id=user.id
    )
    return await ContactsFileSchema.from_tortoise_orm(contact_file_obj)
