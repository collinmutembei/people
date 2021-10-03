from typing import Optional

from fastapi import APIRouter, Depends

from app.core.users import current_active_user
from app.models.socials import SocialAccount, SocialAccountListModel, SocialNetwork
from app.models.users import UserDB

router = APIRouter()


@router.get("", response_model=SocialAccountListModel)
async def all_people(
    network_name: Optional[str] = "", user: UserDB = Depends(current_active_user)
):
    if network_name:
        network = await SocialNetwork.get(name=network_name)
        return await SocialAccountListModel.from_queryset(network.accounts.all())  # type: ignore
    return await SocialAccountListModel.from_queryset(SocialAccount.all())  # type: ignore
