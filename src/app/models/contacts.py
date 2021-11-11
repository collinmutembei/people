from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class ContactsFile(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    uploaded_at = fields.DatetimeField(auto_now_add=True)
    uploader = fields.ForeignKeyField("models.User", related_name="contacts_files")


ContactsFileSchema = pydantic_model_creator(ContactsFile, name="ContactsFile")
