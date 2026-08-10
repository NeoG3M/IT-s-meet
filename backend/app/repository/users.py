from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import SessionDep, get_session
from app.repository.auth import CurrentUser
from app.models import User, UserPrivacySettings, UserSkill
from app.schemas import UserShort
from app.service import check_if_can_show

async def get_short_users(current_user: CurrentUser, session: AsyncSession, faculty: int | None = None, course: int | None = None) -> list[UserShort]:

    query = select(User).outerjoin(UserPrivacySettings)
    # clearing empty users that just added
    query = query.where(User.fullname != "")
    if faculty is not None:
        query = query.where(User.faculty_id == faculty)
    if course is not None:
            query = query.where(User.course == course)

    candidates = await session.execute(query)
    candidates = candidates.scalars().all()

    filtered: List[User] = []
    for u in candidates:
        if check_if_can_show(u, current_user):
            filtered.append(u)

    return [UserShort(**u) for u in filtered]
    

async def create_user(user: User, session: AsyncSession) -> User:
    session.add(user)
    await session.flush()
    await session.commit()
    await session.refresh(user)

    session.add(UserPrivacySettings(user_id=user.id, to_everyone=False, to_faculty=False, to_group=True, to_course=True))
    await session.flush()
    await session.commit()

    return user


async def get_one_user(user_id: int, session: AsyncSession) -> User:
    query = select(User).options(
        selectinload(User.interests),
        selectinload(User.faculty),
        selectinload(User.privacy),
        selectinload(User.user_skills)
            .selectinload(UserSkill.skill),
            selectinload(User.group)).where(User.id == user_id)
    user = await session.execute(query)
    user = user.scalars().one()

    if not user:
        raise HTTPException(status_code=404, detail='User with id {user_id} was not found!')
    return user

