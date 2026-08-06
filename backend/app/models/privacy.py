from datetime import datetime

from sqlalchemy import Integer, String, DateTime, func, ForeignKey, Column, Table, Boolean, text
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database_base import Base

class UserPrivacySettings(Base):
    __tablename__='user_privacy_settings'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    to_everyone: Mapped[bool] = mapped_column(
    Boolean,
    default=False,
    server_default=text("false"),
    nullable=False
    )   

    to_faculty: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default=text("true"),
        nullable=False
    )

    to_group: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default=text("true"),
        nullable=False
    )

    to_course: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default=text("true"),
        nullable=False
    )

    user: Mapped['User'] = relationship('User', back_populates='privacy')

class PostPrivacySettings(Base):
    __tablename__='post_privacy_settings'

    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'), primary_key=True)
    to_everyone: Mapped[bool] = mapped_column(Boolean, server_default=text("false"), default=False)
    to_faculty: Mapped[bool] = mapped_column(Boolean, server_default=text("true"), default=True)
    to_group: Mapped[bool] = mapped_column(Boolean, server_default=text("true"), default=True)
    to_course: Mapped[bool] = mapped_column(Boolean, server_default=text("true"), default=True)

    post: Mapped['Post'] = relationship('Post', back_populates='privacy')

