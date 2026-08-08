from pydantic import BaseModel, ConfigDict, Field

from app.schemas.faculty import FacultyInfo

class GroupShort(BaseModel):
    id: int
    name: str = Field(max_length=50)

    model_config = ConfigDict(from_attributes=True)


class GroupFull(GroupShort):
    faculty: FacultyInfo
    course: int