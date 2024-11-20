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

from inrastructure.sql_database import engine
from inrastructure.sql_database.models.base import Base



class UserGroup(Base):
    __tablename__ = "user_groups"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String(100))
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    users: Mapped[List["AssociationUserUserGroup"]] = relationship(
        back_populates="user_groups")


class Role(Base):
    __tablename__ = "user_group_roles"

    __table_args__ = (
        UniqueConstraint(
            "app",
            "role",
            name="unique_constraint_app_role"),
    )

    id = Column(Integer, primary_key=True, autoincrement="auto")
    app = Column(String(100))
    role = Column(String(100))
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    group: Mapped["UserGroup"] = relationship(
        "UserGroup", back_populates="user_group")
