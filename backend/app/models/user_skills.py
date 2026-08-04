from sqlalchemy import Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database_base import Base

class UserSkill(Base):
    __tablename__ = "user_skills"

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey('skills.id'), primary_key=True)

    level: Mapped[str] = mapped_column(String(32), nullable=True)
    experience: Mapped[int] = mapped_column(Integer, nullable=True)

    user = relationship('User')
    skill = relationship('Skill')