from pydantic import BaseModel, Field


class PostCategoryInfo(BaseModel):
    id: int
    name: str = Field(max_length=64)