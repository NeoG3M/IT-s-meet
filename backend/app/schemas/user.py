from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, ConfigDict

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

    model_config = ConfigDict(from_attributes=True)

class UserShort(BaseModel):
    id: int
    fullname: str = Field(..., max_length=100, min_length=5)

    model_config = ConfigDict(from_attributes=True)

class UserFull(UserShort):
    bio: str
    tg_username: str = Field(max_length=64, min_length=3)
    contacts: UserContacts
    interests: list[InterestInfo] | None
    skills: list[UserSkillInfo] | None
    faculty: FacultyInfo
    course: int
    group: GroupShort
    signed_at: datetime

class CreateUser(BaseModel):
    tg_id: int = Field(ge=0)
    tg_username: str = Field(max_length=64, min_length=3)

class UpdateUser(BaseModel):
    fullname: str | None = Field(max_length=100, min_length=5)
    tg_username: str | None = Field(max_length=64, min_length=3)
    id: int
    bio: str | None
    contacts: UserContacts | None
    interests: list[InterestInfo] | None
    skills: list[UserSkillInfo] | None
    faculty_id: int | None
    group_id: int | None
    course: int | None
    tg_username: str | None = Field(max_length=64, min_length=3)
    privacy: UserPrivacySettings | None