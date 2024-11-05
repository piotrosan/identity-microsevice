import re
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
from inrastructure.database.models import Base


class AgeRange(enum.Enum):
    young = "to 20"
    teacher = "upper than 20 and lower than 60"
    master = "upper 60"

class Sector(enum.Enum):
    it = "IT"
    construction = "Construction"
    gastronomy = "Gastronomy"


class User(Base):

    __tablename__ = "users"

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

    user_groups: Mapped[List["AssociationUserUserGroup"]] = relationship(
        back_populates="user")

    user: Mapped[List["Session"]] = relationship(
        "Session", back_populates="user")

    @validates("email", include_removes=True)
    def validate_email(self, key, email: str, is_remove):
        patter_set = r"[^!#$%&‘*+–/=?\\^_`.{\\|}~ | ^a-zA-Z]"
        local_part, domain, *rest = email.split("@")
        if rest:
            raise ValueError("Invalid email address, contain more than one @")
        if not local_part and not domain:
            raise ValueError("Invalid email address, not contain any of @")
        if len(domain) > 253:
            raise ValueError("Invalid email address, to long domain dns")

        compile_for_invalid_char = re.search(
            patter_set, f"{local_part}{domain}")

        if compile_for_invalid_char:
            raise ValueError(
                f"Invalid email address contain any of "
                f"prohibited char {compile_for_invalid_char.groups()}"
            )
        return email


class ExternalLogin(Base):

    __tablename__ = "external_logins"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    user_id = Column(Integer, ForeignKey("user.id"))
    gmail = Column(BOOLEAN)
    facebook = Column(BOOLEAN)
    client_key = Column(String, nullable=True)
    client_secret = Column(String, nullable=True)
    realms = Column(String, nullable=True)
    redirect_uris = Column(String)
    default_redirect_uri = Column(String)
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    user: Mapped["User"] = relationship("User", back_populates="external_login")
