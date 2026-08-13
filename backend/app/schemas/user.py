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
    # email: EmailStr | None = None
    phone: str | None = None

    model_config = ConfigDict(from_attributes=True)

class UserShort(BaseModel):
    id: int
    fullname: str = Field(max_length=100, default='Not defined')

    model_config = ConfigDict(from_attributes=True)

class UserFull(UserShort):
    bio: str
    tg_username: str = Field(max_length=64, min_length=3)
    contacts: UserContacts
    interests: list[InterestInfo] | None
    skills: list[UserSkillInfo] | None
    faculty: FacultyInfo | None
    course: int
    group: GroupShort | None
    signed_at: datetime

class CreateUser(BaseModel):
    tg_id: int = Field(ge=0)
    tg_username: str = Field(max_length=64, min_length=3)

class UpdateUser(BaseModel):
    fullname: str | None = Field(max_length=100, min_length=5, default=None)
    tg_username: str | None = Field(max_length=64, min_length=3, default=None)
    tg_id: int | None = None
    bio: str | None = None
    contacts: UserContacts | None = None
    faculty_id: int | None = None
    group_id: int | None = None
    course: int | None = None
    privacy: UserPrivacySettings | None = None