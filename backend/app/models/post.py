from datetime import datetime

from sqlalchemy import Integer, String, DateTime, func, ForeignKey, Column, Table, Boolean, text
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database_base import Base

#  Таблицы many-to-many
post_categories = Table(
    'post_categories',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)

post_interests = Table(
    'post_interests',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    Column('interest_id', Integer, ForeignKey('interests.id'), primary_key=True)
)

class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(64), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    active_till: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('true'))
    description: Mapped[str] = mapped_column(TEXT, nullable=False)
    
    importance: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    to_faculty_id: Mapped[int] = mapped_column(ForeignKey("faculties.id"), nullable=True)
    to_course: Mapped[int] = mapped_column(Integer, nullable=True)
    to_group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'), nullable=True)
    privacy: Mapped['PostrPrivacySettings'] = relationship('PostPrivacySettings')

    categories: Mapped[list['Category']] = relationship(secondary=post_categories, back_populates='posts')
    requested_skills: Mapped[list['Skill']] = relationship(secondary='post_skills', back_populates='posts')
    requested_interests: Mapped[list['Interest']] = relationship(secondary=post_interests, back_populates='posts')

    responses: Mapped[list['PostResponse']] = relationship('PostResponse', back_populates='post')
    responses_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    user: Mapped['User'] = relationship("User", back_populates="posts")
    to_faculty: Mapped['Faculty'] = relationship('Faculty')
    to_group: Mapped['Group'] = relationship('Group')