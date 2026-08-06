from pydantic import BaseModel, Field

class UserPrivacySettings(BaseModel):
    to_everyone: bool = Field(default=False)
    to_faculty: bool = Field(default=True)
    to_course: bool = Field(default=True)
    to_group: bool = Field(default=True)