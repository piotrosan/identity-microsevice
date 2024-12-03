import re
import enum
import bcrypt
import uuid
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

from inrastructure.database.sql import engine
from inrastructure.database.sql.models.base import Base


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
    hash_identifier = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=True)
    age_range = Column(Enum(AgeRange), unique=False, nullable=True)
    sector = Column(Enum(Sector), unique=False, nullable=True)
    something_about_me = Column(Text, unique=False, nullable=True)
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    external_logins: Mapped["ExternalLogin"] = relationship(
        back_populates="users")

    user_groups: Mapped[List["AssociationUserUserGroup"]] = relationship(
        back_populates="user")

    # user: Mapped[List["Session"]] = relationship(
    #     "Session", back_populates="users")

    def set_password(self, password):
        self.password = bcrypt.hashpw(password, bcrypt.gensalt())

    def check_password(self, password) -> bool:
        return self.password == bcrypt.hashpw(password, bcrypt.gensalt())

    def set_hash_identifier(self, email: str):
        self.hash_identifier = str(
            uuid.uuid5(namespace=uuid.NAMESPACE_DNS, name=email)
        )

    @validates("sector", include_removes=True)
    def validate_sector(self, key, sector, is_remove):
        sector_enum = Sector(sector)
        if not sector_enum:
            raise ValueError("Invalid sector value")
        return sector_enum

    @validates("age_range", include_removes=True)
    def validate_age_range(self, key, age_range, is_remove):
        age_range_enum = AgeRange(age_range)
        if not age_range_enum:
            raise ValueError("Invalid age range value")
        return age_range_enum

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

        if not compile_for_invalid_char:
            raise ValueError(
                f"Invalid email address contain any of "
                f"prohibited char {compile_for_invalid_char.groups()}"
            )
        return email

class ExternalLogin(Base):

    __tablename__ = "external_logins"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    user_id = Column(Integer, ForeignKey("users.id"))
    gmail = Column(BOOLEAN)
    facebook = Column(BOOLEAN)
    client_key = Column(String, nullable=True)
    client_secret = Column(String, nullable=True)
    realms = Column(String, nullable=True)
    redirect_uris = Column(String)
    default_redirect_uri = Column(String)
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    users: Mapped["User"] = relationship(back_populates="external_logins")
