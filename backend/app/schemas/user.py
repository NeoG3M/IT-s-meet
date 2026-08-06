from datetime import datetime

from pydantic import BaseModel, Field, EmailStr

from app.schemas.skill import UserSkillInfo
from app.schemas.interest import InterestInfo
from app.schemas.faculty import FacultyInfo
from app.schemas.group import GroupShort
from app.schemas.privacy import UserPrivacySettings

class UserContacts(BaseModel):
    vk: str | None = None
    github: str | None = None
    email: EmailStr | None = None
    phone: str | None = None

class UserShort(BaseModel):
    id: int
    fullname: str = Field(..., max_length=100, min_length=5)

class UserFull(UserShort):
    bio: str
    tg_username: str = Field(max_length=64, min_length=3)
    contacts: UserContacts
    interests: list[InterestInfo]
    skills: list[UserSkillInfo]
    faculty: FacultyInfo
    course: int
    group: GroupShort
    signed_at: datetime

class CreateUser(UserFull):
    signed_at: datetime | None
    tg_id: int
    privacy: UserPrivacySettings