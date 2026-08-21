from fastapi import HTTPException
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.auth import CurrentUser
from app.models import User, UserPrivacySettings, UserSkill, Skill, Interest, user_interests
from app.schemas import UserShort
from app.exceptions import raise_user_not_found

async def get_short_users(current_user: CurrentUser, session: AsyncSession, faculty: int | None = None, course: int | None = None) -> list[UserShort]:
    query = select(User).outerjoin(UserPrivacySettings)
    # clearing empty users that just added and not finished
    query = query.where(User.fullname != "").where(User.fullname != "Not defined")
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
        raise_user_not_found(user_id)
    return user


async def patch_user(patched_user_id: int, new_user_info: dict, session: AsyncSession):
    patched_user = await session.execute(select(User).where(User.id == patched_user_id))
    patched_user = patched_user.scalars().one()
    if not patched_user:
         raise_user_not_found(patched_user_id)

    for field, value in new_user_info.items():
         setattr(patched_user, field, value)

    await session.commit()
    await session.refresh(patched_user)

    return patched_user


async def patch_user_skills(patched_user_id: int, new_user_skills: list[dict], session: AsyncSession) -> list[tuple[UserSkill, Skill]]:
    resp = []
    for skill in new_user_skills: 
        if len(skill.keys()) > 1:
            # If patched skill does not even exist, program will skip patch for only one UserSkill
            query = select(Skill).where(Skill.id == skill['id'])
            cur_skill = await session.execute(query)
            cur_skill = cur_skill.scalars().one()
            if not cur_skill:
                continue

            query = select(UserSkill).where(and_(UserSkill.user_id == patched_user_id, UserSkill.skill_id == skill['id']))
            user_skill = await session.execute(query)
            user_skill = user_skill.scalars().one()
            to_update = True
            if not user_skill:
                to_update = False
                user_skill = UserSkill(user_id=patched_user_id, skill_id=skill['id'])

            if 'level' in skill:
                setattr(user_skill, 'level', skill['level'])
            if 'experience' in skill:
                setattr(user_skill, 'experience', skill['experience'])

            if not to_update:
                session.add(user_skill)

            await session.flush()
            await session.commit()
            await session.refresh(user_skill)
            resp.append((user_skill, cur_skill))
    return resp


async def post_user_interests(user_id: int, new_user_interests: list[int], session: AsyncSession) -> list[Interest]:
    resp = []
    for interest_id in new_user_interests:
        interest = await session.execute(select(Interest).where(Interest.id == interest_id))
        interest = interest.scalars().one()
        # If added interest does not even exist, program will skip this part for only one UserInterest
        if not interest:
            continue

        new_connection = user_interests(user_id=user_id, interest_id=interest_id)
        session.add(new_connection)
        await session.flush()
        await session.commit()
        await session.refresh(new_connection)
        resp.append(interest)
