from datetime import datetime

from sqlalchemy import Integer, String, DateTime, func, ForeignKey, Column, Table
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base

post_request_categories = Table(
    'post_request_categories',
    Base.metadata,
    Column('post_request_id', Integer, ForeignKey('posts_request.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)

post_request_interests = Table(
    'post_request_interests',
    Base.metadata,
    Column('post_request_id', Integer, ForeignKey('posts_request.id'), primary_key=True),
    Column('interest_id', Integer, ForeignKey('interests.id'), primary_key=True)
)

class PostRequest(Base):
    __tablename__ = 'posts_request'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(64), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    description: Mapped[str] = mapped_column(TEXT, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    active_till: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    importance: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    categories: Mapped[list['Category']] = relationship(secondary=post_request_categories, back_populates='posts_request')
    to_faculty_id: Mapped[int] = mapped_column(ForeignKey("faculties.id"), nullable=True)
    to_course: Mapped[int] = mapped_column(Integer, nullable=True)
    to_group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'), nullable=True)

    requested_skills: Mapped[list['Skill']] = relationship(secondary='post_request_skills', back_populates='posts_request')
    requested_interests: Mapped[list['Interest']] = relationship(secondary=post_request_interests, back_populates='posts_request')

    
    user: Mapped['User'] = relationship("User", back_populates="posts")
    to_faculty: Mapped['Faculty'] = relationship('Faculty')
    to_group: Mapped['Group'] = relationship('Group')