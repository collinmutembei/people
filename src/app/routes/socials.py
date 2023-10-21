from fastapi import APIRouter

from app.db import SocialAccount, SocialNetwork, User
from app.schemas.socials import (
    SocialAccountCreate,
    SocialAccountRead,
    SocialAccountUpdate,
)

router = APIRouter()


@router.put("/{network_name}", response_model=SocialAccountRead)
async def update_social_network(
    network_name: str, updated_network: SocialAccountUpdate
):
    network = await SocialNetwork.find_one(SocialNetwork.name == network_name)
    await network.set(**updated_network.model_dump(exclude_unset=True))
    return network


@router.post("/{network_name}", response_model=SocialAccountRead)
async def add_social_network_profile(
    network_name: str, account_data: SocialAccountCreate
):
    network = await SocialNetwork.find_one(SocialNetwork.name == network_name)
    user = await User.find_one(User._id == account_data.user._id)
    social_account = await SocialAccount(
        user=user, network=network, username=account_data.username
    )
    return social_account
