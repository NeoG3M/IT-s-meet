from pydantic import BaseModel, Field


class InterestInfo(BaseModel):
    id: int
    name: str = Field(max_length=50)