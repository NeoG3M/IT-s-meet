from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database_base import Base


class Skill(Base):
    __tablename__ = 'skills'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    user_skills: Mapped[list['UserSkill']] = relationship('UserSkill', back_populates='skill', cascade="all")
    post_skills: Mapped[list['PostSkill']] = relationship('PostSkill', back_populates='skill', cascade="all")