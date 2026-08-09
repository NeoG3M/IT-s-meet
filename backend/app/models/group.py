from sqlalchemy import Integer, String, ForeignKey, Null
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database_base import Base


class Group(Base):
    __tablename__= "groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    faculty_id: Mapped[int | Null] = mapped_column(ForeignKey("faculties.id"))
    course: Mapped[int | Null] = mapped_column(Integer)

    users = relationship("User", back_populates="group")
    faculty = relationship("Faculty")
    posts = relationship('Post', back_populates='to_group')