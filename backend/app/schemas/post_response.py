from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.user import UserShort
    

class PostResponse(BaseModel):
    id: int
    created_at: datetime
    is_accepted: bool = Field(default=False)
    user: UserShort | None
    is_watched: bool | None = Field(default=False)
    message: str | None = Field(max_length=128)