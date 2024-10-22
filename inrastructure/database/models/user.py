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
    Enum
)

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.orm import validates

from inrastructure.database import engine
from inrastructure.database.models.base import Base


association_table = Table(
    "user_group_association_table",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("group_id", ForeignKey("user_group.id"), primary_key=True),
)


class AgeRange(enum.Enum):
    young = "to 20"
    teacher = "upper than 20 and lower than 60"
    master = "upper 60"

class Sector(enum.Enum):
    it = "IT"
    construction = "Construction"
    gastronomy = "Gastronomy"

class User(Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=True)
    age_range = Column(Enum(AgeRange), unique=False, nullable=True)
    sector = Column(Enum(Sector), unique=False, nullable=True)
    something_about_me = Column(Text, unique=False, nullable=True)
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    external_login: Mapped["ExternalLogin"] = relationship(
        "ExternalLogin", back_populates="user")

    user_groups: Mapped["UserGroup"] = relationship(
        secondary=association_table, back_populates="user_groups")

    @validates("email", include_removes=True)
    def validate_address(self, key, email, is_remove):
        # todo insert validation method for this like as on endpoint for react
        if "@" not in email:
            raise ValueError("failed simplified email validation")
        return email


class ExternalLogin(Base):

    __tablename__ = "external_login"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    user_id = Column(Integer, ForeignKey("user.id"))
    gmail = Column(BOOLEAN)
    facebook = Column(BOOLEAN)
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    user: Mapped["User"] = relationship("User", back_populates="external_login")


Base.metadata.create_all(engine)
