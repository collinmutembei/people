from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models.mixins import TimestampMixin


class ContactsFile(TimestampMixin, models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    uploader = fields.ForeignKeyField("models.User", related_name="contacts_files")


ContactsFileSchema = pydantic_model_creator(ContactsFile, name="ContactsFile")
