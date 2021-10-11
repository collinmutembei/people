from fastapi import Depends
from fastapi_crudrouter.core.tortoise import TortoiseCRUDRouter

from app.core.users import current_active_user
from app.models.socials import (
    SocialAccount,
    SocialAccountCreateModel,
    SocialAccountModel,
    SocialNetwork,
    SocialNetworkCreateModel,
    SocialNetworkModel,
)
from app.models.users import User

social_network_router = TortoiseCRUDRouter(
    schema=SocialNetworkModel,
    create_schema=SocialNetworkCreateModel,
    update_schema=SocialNetworkCreateModel,
    db_model=SocialNetwork,
    dependencies=[Depends(current_active_user)],
    get_one_route=False,
    delete_one_route=False,
    delete_all_route=False,
    prefix="/socialnetwork",
)


@social_network_router.post("/{network_name}", response_model=SocialAccountModel)
async def add_social_network_profile(
    network_name: str, account_data: SocialAccountCreateModel
):
    network = await SocialNetwork.get(name=network_name)
    user = await User.get(id=account_data.user_id)
    social_account = await SocialAccount.create(
        user=user, network=network, username=account_data.username
    )
    return await SocialAccountModel.from_tortoise_orm(social_account)
