from sqlalchemy import Integer, String, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class Faculty(Base):
    __tablename__= "faculties"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    users = relationship("User", back_populates="Faculty")
    groups = relationship('Group', back_populates='Faculty')