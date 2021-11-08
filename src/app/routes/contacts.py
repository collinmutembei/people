from fastapi import APIRouter, Depends, File, UploadFile

from app.core.users import fastapi_users
from app.models.contacts import ContactsFile, ContactsFileSchema
from app.utils import get_storage_client

router = APIRouter()


@router.post("/upload")
async def upload_contacts(
    contacts: UploadFile = File(...),
    user=Depends(fastapi_users.current_user(active=True)),
    storage_client=Depends(get_storage_client),
):
    # TODO: Read CSV file and create users and social accounts
    contact_file_obj = await ContactsFile.create(
        name=contacts.filename, uploader_id=user.id
    )
    return await ContactsFileSchema.from_tortoise_orm(contact_file_obj)
