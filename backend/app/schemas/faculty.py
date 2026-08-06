from pydantic import BaseModel, Field

class FacultyInfo(BaseModel):
    id: int
    name: str = Field(max_length=100)

class FacultyFull(FacultyInfo):
    users_count: int
    posts_count: int
    active_posts_count: int