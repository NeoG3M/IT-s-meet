from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database_base import Base


class Skill(Base):
    __tablename__ = 'skills'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    users: Mapped[list['User']] = relationship(secondary='user_skills', back_populates='skills')