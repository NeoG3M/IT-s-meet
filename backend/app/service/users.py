from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.schemas import CreateUser, UserFull, UserContacts, FacultyInfo, InterestInfo, UserSkillInfo, GroupShort
from app.models import User
from app.repository import create_user, get_one_user

async def user_creation(user_data: CreateUser, session: AsyncSession) -> User:
    sign_date = datetime.now()
    new_user = User(tg_id=user_data.tg_id, tg_username=user_data.tg_username, signed_at=sign_date)
    new_user = await create_user(new_user, session)

    return new_user


async def chech_if_can_show(who: User, to: User) -> bool:
    is_shown = False
    
    if who.privacy.to_everyone:
        is_shown = True 

    if who.privacy.to_faculty and to.faculty_id == who.faculty_id:
        is_shown = True 

    if who.privacy.to_group and to.group_id == who.group_id:
        is_shown = True

    if who.privacy.to_course and to.faculty_id == who.faculty_id and to.course == who.course:
        is_shown = True

    return is_shown


async def giving_one_user(user_id: int, current_user: User, session: AsyncSession) -> UserFull:
    wanted_user = await get_one_user(user_id, session)
    if not chech_if_can_show(wanted_user, current_user):
        raise HTTPException(status_code=451, detail="Wanted user's privacy settings doesn't allow to show pesronal information to current user.")

    # Preparing different schemas to load into final UserFull scheme
    user_contacts = UserContacts(**wanted_user.contacts)
    user_interests = [InterestInfo(id=it.id, name=it.name) for it in wanted_user.interests]
    user_skills = [UserSkillInfo(id=rel.skill_id, name=rel.skill.name, level=rel.level, experience=rel.experience) for rel in wanted_user.user_skills]
    user_faculty = FacultyInfo(id=wanted_user.faculty_id, name=wanted_user.faculty.name)
    user_group = GroupShort(id=wanted_user.group_id, name=wanted_user.group.name)

    sent_user_info = UserFull(id=wanted_user.id, 
                            fullname=wanted_user.fullname, 
                            bio=wanted_user.bio,
                            tg_username=wanted_user.tg_username, 
                            contacts=user_contacts,
                            interests=user_interests,
                            skills=user_skills,
                            faculty=user_faculty,
                            course=wanted_user.course,
                            group=user_group,
                            signed_at=wanted_user.signed_at)
    return sent_user_info