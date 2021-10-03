from uuid import UUID

from pydantic import BaseModel
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from app.models.mixins import TimestampMixin


class SocialAccount(TimestampMixin, models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    network = fields.ForeignKeyField("models.SocialNetwork", related_name="accounts")
    user = fields.ForeignKeyField("models.User", related_name="social_accounts")

    @property
    async def url(self) -> str:
        from app.utils import get_account_url  # noqa

        social_network = await self.network
        return get_account_url(social_network, self)

    async def __str__(self):
        return await self.url

    class Meta:
        unique_together = (("username", "network"),)


SocialAccountModel = pydantic_model_creator(SocialAccount, name="SocialAccountModel")

SocialAccountListModel = pydantic_queryset_creator(SocialAccount)


class SocialAccountCreateModel(BaseModel):
    username: str
    user_id: UUID


class SocialNetwork(TimestampMixin, models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=20, unique=True)
    domain = fields.CharField(max_length=50, null=True)
    account_prefix = fields.CharField(max_length=30, null=True)

    def __str__(self):
        return f"{self.name}: https://{self.domain}"


SocialNetworkModel = pydantic_model_creator(SocialNetwork, name="SocialNetworkModel")


SocialNetworkCreateModel = pydantic_model_creator(
    SocialNetwork, name="SocialNetworkCreateModel", exclude_readonly=True
)
