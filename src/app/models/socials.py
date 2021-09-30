from enum import Enum

from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class SocialAccountServiceProviders(Enum):
    FACEBOOK = "facebook"
    TWITTER = "twitter"
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"
    YOUTUBE = "youtube"


class SocialAccountService(models.Model):
    id = fields.IntField(pk=True)
    domain = fields.CharField(max_length=50, null=True)
    provider = fields.CharEnumField(enum_type=SocialAccountServiceProviders)


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


SocialAccountModel = pydantic_model_creator(SocialAccount, name="SocialAccountModel")
SocialAccountCreateModel = pydantic_model_creator(
    SocialAccount, name="SocialAccountCreateModel", exclude_readonly=True
)
