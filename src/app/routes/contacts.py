from fastapi import APIRouter, Depends, File, UploadFile

from app.core.users import fastapi_users
from app.models.contacts import ContactsFile, ContactsFileSchema

router = APIRouter()


@router.post("/upload")
async def upload_contacts(
    contacts: UploadFile = File(...),
    user=Depends(fastapi_users.current_user(active=True)),
):
    #  TODO: Read CSV file and create users and social accounts
    contact_file_obj = await ContactsFile.create(name=contacts.filename, user=user)
    return await ContactsFileSchema.from_tortoise_orm(contact_file_obj)
