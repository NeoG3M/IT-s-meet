from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database_base import Base

class PostSkill(Base):
    __tablename__ = "post_skills"

    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'), primary_key=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey('skills.id'), primary_key=True)

    level: Mapped[str] = mapped_column(String(32), nullable=True)
    experience: Mapped[int] = mapped_column(Integer, nullable=True)

    post: Mapped['Post'] = relationship('Post', back_populates='requested_skills')
    skill: Mapped['Skill'] = relationship('Skill', back_populates='post_skills')