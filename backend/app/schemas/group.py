from pydantic import BaseModel, Field

from app.schemas.faculty import FacultyInfo

class GroupShort(BaseModel):
    id: int
    name: str = Field(max_length=50)


class GroupFull(GroupShort):
    faculty: FacultyInfo
    course: int