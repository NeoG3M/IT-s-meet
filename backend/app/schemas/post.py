from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from app.schemas.user import UserShort
from app.schemas.category import PostCategoryInfo
from app.schemas.skill import SkillShort
from app.schemas.interest import InterestInfo
from app.schemas.faculty import FacultyInfo
from app.schemas.group import GroupShort
from app.schemas.post_response import PostResponse

class PostShort(BaseModel):
    id: int
    title: str = Field(max_length=64)
    user: UserShort
    acive_till: datetime
    importance: int
    categories: list[PostCategoryInfo]
    skills: list[SkillShort]
    interests: list[InterestInfo]
    responses_count: int = Field(ge=0, default=0)

    @field_validator('importance')
    def validate_importance(importance: int):
        if not (0 <= importance <= 5):
            raise ValueError(f'Importance can be only beetwen 0 and 5. {importance} was given.')
        return importance


class PostFull(PostShort):
    created_at: datetime
    description: str
    faculty: FacultyInfo
    course: int = Field(gt=0)
    group: GroupShort
    responses: list[PostResponse]

