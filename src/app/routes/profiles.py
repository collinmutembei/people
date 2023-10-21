from typing import List, Optional

from beanie.operators import In
from fastapi import APIRouter, Depends

from app.core.users import current_active_user
from app.db import SocialAccount, SocialNetwork, User
from app.schemas.socials import SocialAccountRead

router = APIRouter()


@router.get("", response_model=Optional[List[SocialAccountRead]])
async def all_social_profiles(
    network_name: Optional[str] = "", user: User = Depends(current_active_user)
):
    if network_name:
        network = await SocialNetwork.find(name=network_name)
        return await SocialAccount.find(In(user._id, network.accounts)).to_list()
