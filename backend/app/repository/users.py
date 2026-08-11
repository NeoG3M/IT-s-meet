from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.auth import CurrentUser
from app.models import User, UserPrivacySettings, UserSkill
from app.schemas import UserShort, UpdateUser

async def get_short_users(current_user: CurrentUser, session: AsyncSession, faculty: int | None = None, course: int | None = None) -> list[UserShort]:
    query = select(User).outerjoin(UserPrivacySettings)
    # clearing empty users that just added and not finished
    query = query.where(User.fullname != "")
    if faculty is not None:
        query = query.where(User.faculty_id == faculty)
    if course is not None:
            query = query.where(User.course == course)

    users = await session.execute(query)
    users = users.scalars().all()

    return users
    

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


async def patch_user(patched_user: int, new_user_info: dict, session: AsyncSession):
    for field, value in new_user_info.items():
         setattr(patched_user, field, value)

    await session.commit()
    await session.refresh(patched_user)

    return patch_user
    