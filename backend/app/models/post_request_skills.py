from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base

class PostRequestSkill(Base):
    __tablename__ = "post_request_skills"

    post_request_id: Mapped[int] = mapped_column(ForeignKey('posts_request.id'), primary_key=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey('skills.id'), primary_key=True)

    level: Mapped[str] = mapped_column(String(32), nullable=True)
    experience: Mapped[int] = mapped_column(Integer, nullable=True)

    post_request: Mapped['PostRequest'] = relationship('PostRequest')
    skill: Mapped['Skill'] = relationship('Skill')