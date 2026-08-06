from pydantic import BaseModel, Field

class SkillShort(BaseModel):
    id: int
    name: str = Field(max_length=50, min_length=1)

class UserSkillInfo(SkillShort):
    level: str = Field(max_length=32, min_length=1)
    experience: int = Field(ge=1)