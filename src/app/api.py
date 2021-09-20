from fastapi import Depends, FastAPI
from fastapi_pagination import LimitOffsetPage, add_pagination, paginate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db import get_session
from app.models import Profile, ProfileCreate

api = FastAPI()


@api.get("/people", response_model=LimitOffsetPage[Profile])
async def get_people(session: AsyncSession = Depends(get_session)):
    """
    Return all people
    """
    result = await session.execute(select(Profile))
    people = result.scalars().all()
    return paginate(
        [
            Profile(
                first_name=person.first_name,
                last_name=person.last_name,
                surname=person.surname,
                id=person.id,
            )
            for person in people
        ]
    )


@api.post("/people")
async def add_person(
    person: ProfileCreate, session: AsyncSession = Depends(get_session)
):
    """
    Add a person
    """
    profile = Profile(
        first_name=person.first_name, last_name=person.last_name, surname=person.surname
    )
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    return profile


add_pagination(api)
