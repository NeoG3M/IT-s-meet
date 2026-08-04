from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database_base import Base


class Faculty(Base):
    __tablename__= "faculties"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    users = relationship("User", back_populates="faculty")
    groups = relationship('Group', back_populates='faculty')
    posts = relationship('Post', back_populates='to_faculty')