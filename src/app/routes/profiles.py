from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends

from app.core.users import current_active_user
from app.db import SocialAccount, SocialNetwork, User
from app.schemas.socials import SocialAccountCreate, SocialAccountRead

router = APIRouter()


@router.get("", response_model=Optional[List[SocialAccountRead]])
async def all_social_profiles(
    network_name: Optional[str] = "", user: User = Depends(current_active_user)
):
    network = await SocialNetwork.find_one(SocialNetwork.name == network_name)
    if network:
        social_accounts = await SocialAccount.find(
            SocialAccount.network.name == network.name, fetch_links=True
        ).to_list()
        return social_accounts


@router.post("", response_model=SocialAccountRead)
async def add_social_profile(
    user_id: str,
    profile_details: SocialAccountCreate,
    user: User = Depends(current_active_user),
):
    network = await SocialNetwork.find_one(
        SocialNetwork.name == profile_details.network_name
    )
    profile_user = await User.get(user_id)
    if network and profile_user:
        social_account = await SocialAccount(
            username=profile_details.username,
            network=network,
            user=profile_user,
            modified_at=datetime.utcnow(),
            created_by=user,
        ).insert()
        return social_account
