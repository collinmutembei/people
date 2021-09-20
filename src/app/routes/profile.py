from fastapi import APIRouter, Depends
from fastapi_pagination import LimitOffsetPage, paginate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db import get_session
from app.models import Profile, ProfileCreate, ProfileUpdate

router = APIRouter()


@router.get("/", response_model=LimitOffsetPage[Profile])
async def get_people(session: AsyncSession = Depends(get_session)):
    """
    Return all people
    """
    result = await session.execute(select(Profile))
    people = result.scalars().all()
    return paginate(people)


@router.post("/", response_model=Profile)
async def add_person(
    person: ProfileCreate, session: AsyncSession = Depends(get_session)
):
    """
    Add a person
    """
    profile = Profile(first_name=person.first_name, last_name=person.last_name)
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    return profile


@router.put("/", response_model=Profile)
async def update_person(
    person: ProfileUpdate, session: AsyncSession = Depends(get_session)
):
    """
    Update a person
    """
    profile = Profile(first_name=person.first_name, last_name=person.last_name)
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    return profile


@router.delete("/")
async def delete_person(
    person: ProfileUpdate, session: AsyncSession = Depends(get_session)
):
    """
    Delete a person
    """
    profile = Profile(first_name=person.first_name, last_name=person.last_name)
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    return profile
