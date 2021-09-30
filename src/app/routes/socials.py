from fastapi import Depends
from fastapi_crudrouter.core.tortoise import TortoiseCRUDRouter

from app.core.users import current_active_user
from app.models.socials import (
    SocialAccount,
    SocialAccountCreateModel,
    SocialAccountModel,
    SocialAccountService,
    SocialAccountServiceCreateModel,
    SocialAccountServiceModel,
)

service_router = TortoiseCRUDRouter(
    schema=SocialAccountServiceModel,
    create_schema=SocialAccountServiceCreateModel,
    db_model=SocialAccountService,
    dependencies=[Depends(current_active_user)],
    get_one_route=False,
    delete_all_route=False,
    prefix="/socialnetwork",
)

account_router = TortoiseCRUDRouter(
    schema=SocialAccountModel,
    create_schema=SocialAccountCreateModel,
    db_model=SocialAccount,
    dependencies=[Depends(current_active_user)],
    delete_all_route=False,
    prefix="/socialaccount",
)


@account_router.post("", response_model=SocialAccountModel)
async def create_social_account(social_account: SocialAccountCreateModel):
    # TODO: create account using logged in user
    pass
