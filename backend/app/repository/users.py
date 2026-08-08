from typing import List

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.database import SessionDep
from app.repository.auth import CurrentUser
from app.models import User, UserPrivacySettings
from app.schemas import UserShort

async def get_short_users(current_user: CurrentUser, session: SessionDep, faculty: int | None = None, course: int | None = None):
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
    

async def create_user(user: User, session: SessionDep):
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user
