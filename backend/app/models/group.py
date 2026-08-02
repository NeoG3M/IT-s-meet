from datetime import datetime

from sqlalchemy import Integer, String, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class Group(Base):
    __tablename__= "groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    faculty_id: Mapped[int] = mapped_column(ForeignKey("faculties.id"), primary_key=True)
    course: Mapped[int] = mapped_column(Integer, nullable=False)

    users = relationship("Users", back_populates="Group")
    faculty = relationship("Faculty")