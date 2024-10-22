import enum
from typing import List

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Text,
    BOOLEAN,
    ForeignKey,
    Table,
    Enum,
    UniqueConstraint
)

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from inrastructure.database import engine
from inrastructure.database.models.base import Base


from .user import association_table


class UserGroupName(enum.Enum):
    student = "Student"
    teacher = "Teacher"
    master = "Master"


class APPName(enum.Enum):
    flashcard = "FlashCard"
    exercise = "Exercise"
    wisdom = "Wisdom"


class UserGroup(Base):
    __tablename__ = "user_group"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(Enum(UserGroupName))
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    user: Mapped[List["User"]] = relationship(
        secondary=association_table, back_populates="user")


class Role(Base):
    __tablename__ = "user_group_role"

    __table_args__ = (
        UniqueConstraint(
            "app",
            "role",
            name="unique_constraint_app_role"),
    )

    id = Column(Integer, primary_key=True, autoincrement="auto")
    app = Column(Enum(APPName))
    role = Column(String(255))
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    group: Mapped["UserGroup"] = relationship(
        "UserGroup", back_populates="user_group")

Base.metadata.create_all(engine)