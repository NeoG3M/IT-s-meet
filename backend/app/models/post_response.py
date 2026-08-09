from datetime import datetime

from sqlalchemy import Integer, String, DateTime, func, ForeignKey, Column, Table, Boolean
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database_base import Base


class PostResponse(Base):
    __tablename__ = 'post_responses'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    message: Mapped[str] = mapped_column(String(128), nullable=False, default='')

    is_watched: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_accepted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    post: Mapped['Post'] = relationship('Post', back_populates='responses')
    user: Mapped['User'] = relationship('User', back_populates='responses')