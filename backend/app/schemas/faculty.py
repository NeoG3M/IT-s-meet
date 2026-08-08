from pydantic import BaseModel, ConfigDict, Field

class FacultyInfo(BaseModel):
    id: int
    name: str = Field(max_length=100)
    model_config = ConfigDict(from_attributes=True)

class FacultyFull(FacultyInfo):
    users_count: int
    posts_count: int
    active_posts_count: int