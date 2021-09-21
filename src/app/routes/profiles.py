from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import LimitOffsetPage, paginate
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db import get_session
from app.models import Profile as ProfileModel
from app.schemas import Profile, ProfileDetails, ProfileStatus

router = APIRouter()


@router.get("/", response_model=LimitOffsetPage[Profile])
async def get_profiles(session: AsyncSession = Depends(get_session)):
    """
    Return all profiles
    """
    query = await session.execute(
        select(ProfileModel).where(ProfileModel.active == True)  # noqa: E712
    )
    profiles = query.scalars().all()
    return paginate(
        [Profile(id=p.id, name=p.name, bio=p.bio, active=p.active) for p in profiles]
    )


@router.post("/", response_model=Profile)
async def add_profile(
    profile_data: ProfileDetails, session: AsyncSession = Depends(get_session)
):
    """
    Add a profile
    """
    profile = ProfileModel(**profile_data.dict())
    try:
        session.add(profile)
        await session.commit()
    except exc.IntegrityError:
        raise HTTPException(
            status_code=400, detail=f"Profile with name {profile.name} already exists."
        )
    await session.refresh(profile)
    return profile


@router.put("/{profile_uuid}", response_model=Profile)
async def update_profile(
    profile_uuid: UUID,
    updated_profile: ProfileDetails,
    session: AsyncSession = Depends(get_session),
):
    """
    Update a profile
    """
    # TODO: Update object
    query = await session.execute(
        select(ProfileModel).where(ProfileModel.id == profile_uuid)
    )
    profile = query.scalars().first()
    # profile.name = update_profile.name
    # profile.bio = update_profile.bio
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    return profile


@router.delete("/{profile_uuid}", response_model=ProfileStatus)
async def deactivate_profile(
    profile_uuid: UUID, session: AsyncSession = Depends(get_session)
):
    """
    Deactivates a profile
    """
    query = await session.execute(
        select(ProfileModel).where(ProfileModel.id == profile_uuid)
    )
    profile = query.scalars().first()
    # make indempotent
    if profile.active == True:  # noqa: E712
        profile.active = False
        session.add(profile)
        await session.commit()
        await session.refresh(profile)
    return ProfileStatus(id=profile.id, active=profile.active)
