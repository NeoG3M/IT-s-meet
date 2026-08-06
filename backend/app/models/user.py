from datetime import datetime

from sqlalchemy import Integer, String, DateTime, func, ForeignKey, TEXT, Table, Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database_base import Base

user_interests = Table(
    "user_interests",
    Base.metadata,
    Column("user_id", ForeignKey('users.id'), primary_key=True),
    Column('interest_id', ForeignKey('interests.id'), primary_key=True)
)

class User(Base):
    __tablename__= "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fullname: Mapped[str] = mapped_column(String(100), nullable=False)
    tg_id: Mapped[int] = mapped_column(Integer, nullable=False)
    tg_username: Mapped[str] = mapped_column(String(64), nullable=False)
    contacts: Mapped[dict[str, any]] = mapped_column(JSONB, nullable=False, default=dict)
    faculty_id: Mapped[int] = mapped_column(ForeignKey("faculties.id"), nullable=False)
    course: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), nullable=False)
    bio: Mapped[str] = mapped_column(TEXT, nullable=False, default="")
    signed_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    privacy: Mapped['UserPrivacySettings'] = relationship('UserPrivacySettings', uselist=False, cascade="all, delete-orphan", back_populates='user')

    user_skills: Mapped[list["UserSkill"]] = relationship(secondary="user_skills", back_populates="users")
    interests: Mapped[list["Interest"]] = relationship(secondary=user_interests, back_populates="users")
    responses: Mapped[list["PostResponse"]] = relationship("PostResponse", back_populates="user")
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="user")

    faculty = relationship("Faculty")
    group = relationship("Group")