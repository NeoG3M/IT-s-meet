from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.schemas import CreateUser, UserFull, UserContacts, FacultyInfo, InterestInfo, UserSkillInfo, GroupShort, UserShort, UpdateUser, UpdateUserSkill
from app.models import User
from app.repository import create_user, get_one_user, patch_user, get_short_users, patch_user_skills
from app.exceptions import raise_rights_exceptions

async def user_creation(user_data: CreateUser, session: AsyncSession) -> User:
    sign_date = datetime.now()
    new_user = User(tg_id=user_data.tg_id, tg_username=user_data.tg_username, signed_at=sign_date)
    new_user = await create_user(new_user, session)

    return new_user


def check_if_can_show(who: User, to: User) -> bool:
    if not (to.privacy and who.privacy):
        return False
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

async def giving_all_users_short(current_user: User, session: AsyncSession, faculty: int | None = None, course: int | None = None) -> list[UserShort]:
    users_list = await get_short_users(current_user=current_user, session=session, faculty=faculty, course=course)
    filtered: list[User] = []
    for u in users_list:
        if check_if_can_show(u, current_user):
            filtered.append(u)

    return [UserShort(**u) for u in filtered]


# Preparing different schemas to load into final UserFull scheme
def compact_user_to_full(user: User) -> UserFull:
    user_contacts = UserContacts(**user.contacts)
    try:
        if user.interests:
            user_interests = [InterestInfo(id=it.id, name=it.name) for it in user.interests]
        else:
            user_interests = None
    except Exception:
        user_interests = None

    try:
        if user.user_skills:
            user_skills = [UserSkillInfo(id=rel.skill_id, name=rel.skill.name, level=rel.level, experience=rel.experience) for rel in user.user_skills]
        else:
            user_skills = None
    except Exception:
            user_skills = None

    try:
        if user.faculty:
            user_faculty = FacultyInfo(id=user.faculty_id, name=user.faculty.name)
        else:
            user_faculty = None
    except Exception:
        user_faculty = None

    try:
        if user.group:
            user_group = GroupShort(id=user.group_id, name=user.group.name)
        else:
            user_group = None
    except Exception:
        user_group = None
    
    sent_user_info = UserFull(id=user.id, 
                            fullname=user.fullname, 
                            bio=user.bio,
                            tg_username=user.tg_username, 
                            contacts=user_contacts,
                            interests=user_interests,
                            skills=user_skills,
                            faculty=user_faculty,
                            course=user.course,
                            group=user_group,
                            signed_at=user.signed_at)
    return sent_user_info


async def giving_one_user(user_id: int, current_user: User, session: AsyncSession) -> UserFull:
    wanted_user = await get_one_user(user_id, session)
    if not check_if_can_show(wanted_user, current_user):
        raise HTTPException(status_code=403, detail="Wanted user's privacy settings doesn't allow to show pesronal information to current user.")

    sent_user_info = compact_user_to_full(user=wanted_user)
    return sent_user_info

async def try_patch_user(user_id: int, current_user: User, session: AsyncSession, new_user_info: UpdateUser) -> UserFull:
    # TODO: add admin rights checking
    if user_id != current_user.id:
        raise_rights_exceptions()

    user_new_data = new_user_info.model_dump(exclude_unset=True)
    if 'fullname' in user_new_data and len(user_new_data['fullname']) < 5:
        raise ValueError("User's fullname should be at least 5 characters long.")

    patched_user = await patch_user(patched_user_id=user_id, session=session, new_user_info=user_new_data)
    full = compact_user_to_full(patched_user)
    return full

async def try_patch_user_skills(user_id: int, current_user: User, session: AsyncSession, new_user_skills: list[UpdateUserSkill]) -> list[UserSkillInfo]:
    # TODO: add admin rights checking
    if user_id != current_user.id:
        raise_rights_exceptions()
    # Just check user existence
    await get_one_user(user_id=user_id, session=session)

    dumped = [sk.model_dump(exclude_unset=True) for sk in new_user_skills]
    resp = await patch_user_skills(patched_user_id=user_id, new_user_skills=dumped, session=session)
    output = []
    for user_skill, skill in resp:
        info = UserSkillInfo(id=skill.id, name=skill.name, level=user_skill.level, experience=user_skill.level)
        output.append(info)
    return output