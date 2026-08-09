from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import SessionDep, get_session
from app.repository.auth import CurrentUser
from app.models import User, UserPrivacySettings
from app.schemas import UserShort

async def get_short_users(current_user: CurrentUser, session: AsyncSession, faculty: int | None = None, course: int | None = None):

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
        is_shown = False

        if u.privacy.to_everyone:
            is_shown = True 

        if u.privacy.to_faculty and current_user.faculty_id == u.faculty_id:
            is_shown = True 

        if u.privacy.to_group and current_user.group_id == u.group_id:
            is_shown = True

        if u.privacy.to_course and current_user.faculty_id == u.faculty_id and current_user.course == u.course:
            is_shown = True

        if is_shown:
            filtered.append(u)

    return [UserShort(**u) for u in filtered]
    

async def create_user(user: User, session: AsyncSession):
    session.add(user)
    await session.flush()
    await session.commit()
    await session.refresh(user)

    return user


async def get_one_user(user_id: int, session: AsyncSession):
    query = select(User).where(User.id == user_id)
    user = await session.execute(query)
    user = user.scalars().one()

    if not user:
        raise HTTPException(status_code=404, detail='User with id {user_id} was not found!')
    

