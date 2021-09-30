from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models.users import UserBaseModel, UserModel


class SocialAccountService(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=20, unique=True)
    domain = fields.CharField(max_length=50, null=True)


class SocialAccount(models.Model):
    id = fields.UUIDField(pk=True)
    address = fields.CharField(max_length=20, unique=True)
    service = fields.ForeignKeyField(
        "models.SocialAccountService", related_name="accounts"
    )
    user = fields.ForeignKeyField("models.User", related_name="social_accounts")
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    async def url(self) -> str:
        service_domain = await self.service.domain  # type: ignore
        return f"{service_domain}/{self.address}"

    class PydanticMeta:
        computed = ["url"]


SocialAccountServiceModel = pydantic_model_creator(
    SocialAccountService, name="SocialAccountServiceModel"
)


SocialAccountServiceCreateModel = pydantic_model_creator(
    SocialAccountService, name="SocialAccountServiceCreateModel", exclude_readonly=True
)


class SocialAccountServiceReadModel(BaseModel):
    name: str


# SocialAccountSchema = pydantic_model_creator(SocialAccount, name="SocialAccountSchema")


class SocialAccountModel(BaseModel):
    id: UUID
    service: SocialAccountServiceReadModel
    user: UserModel
    created_at: datetime
    modified_at: datetime
    url: str


class SocialAccountCreateModel(BaseModel):
    address: str
    service: SocialAccountServiceReadModel
    user: UserBaseModel
