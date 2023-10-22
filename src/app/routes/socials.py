from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends

from app.core.users import current_active_user
from app.db import SocialNetwork, User
from app.schemas.socials import (
    SocialNetworkCreate,
    SocialNetworkRead,
    SocialNetworkUpdate,
)

router = APIRouter()


@router.get("", response_model=List[SocialNetworkRead])
async def get_social_networks():
    networks = await SocialNetwork.find_all(fetch_links=True).to_list()
    return networks


@router.post("", response_model=SocialNetworkRead)
async def add_social_network(
    social_network: SocialNetworkCreate, user: User = Depends(current_active_user)
):
    network = await SocialNetwork(
        **social_network.model_dump(), modified_at=datetime.utcnow(), created_by=user
    ).insert()
    return network


@router.put("/{network_name}", response_model=Optional[SocialNetworkRead])
async def update_social_network(
    network_name: str,
    updated_network: SocialNetworkUpdate,
    user: User = Depends(current_active_user),
):
    network = await SocialNetwork.find(
        SocialNetwork.name == network_name
    ).first_or_none()
    if network:
        await network.set(
            {
                SocialNetwork.name: updated_network.name or network.name,
                SocialNetwork.domain: updated_network.domain or network.domain,
                SocialNetwork.account_prefix: updated_network.account_prefix
                or network.account_prefix,
            }
        )
        network.modified_at = datetime.utcnow()
        network.modified_by = user
        await network.save()
        return network
