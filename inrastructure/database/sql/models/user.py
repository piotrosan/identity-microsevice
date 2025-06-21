import re
import enum
import bcrypt
import uuid
from typing import List

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    Enum,
    JSON, LargeBinary
)
from sqlalchemy.dialects.postgresql import BYTEA

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

from inrastructure.database.sql.exception.user import HttpUserModelException
from inrastructure.database.sql.models.base import Base
from inrastructure.database.sql.models.mixins import CreatedUpdatedMixin
from inrastructure.security.jwt.token import TokenFactory, AccessToken, \
    RefreshToken


class AgeRange(enum.Enum):
    young = "to 20"
    teacher = "upper than 20 and lower than 60"
    master = "upper 60"


class User(CreatedUpdatedMixin, Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    hash_identifier = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(LargeBinary, nullable=True)
    age_range = Column(Enum(AgeRange), unique=False, nullable=True)
    additional_info = Column(Text, unique=False, nullable=True)

    external_logins: Mapped["ExternalLogin"] = relationship(
        back_populates="users"
    )

    @classmethod
    def bcrypt_pass(cls, password: str):
        return bcrypt.hashpw(
            password.encode('UTF-8'),
            bcrypt.gensalt(10)
        )

    def check_password(self, password: str) -> bool:
        if not bcrypt.checkpw(
                password.encode('UTF-8'),
                self.password
        ):
            raise HttpUserModelException(
                detail='Password doesnt match', status_code=400
            )
        return True

    def set_hash_identifier(self, email: str):
        self.hash_identifier = str(
            uuid.uuid5(namespace=uuid.NAMESPACE_DNS, name=email)
        )

    @validates("age_range", include_removes=True)
    def validate_age_range(self, key, age_range, is_remove):
        age_range_enum = AgeRange(age_range)
        if not age_range_enum:
            raise ValueError("Invalid age range value")
        return age_range_enum

    @validates("email", include_removes=True)
    def validate_email(self, key, email: str, is_remove):
        patter_set = r"[^!#$%&‘*+–/=?\\^_`.{\\|}~]"
        local_part, domain, *rest = email.split("@")
        if rest:
            raise ValueError("Invalid email address, contain more than one @")
        if not local_part and not domain:
            raise ValueError("Invalid email address, not contain any of @")
        if len(domain) > 253:
            raise ValueError("Invalid email address, to long domain dns")

        compile_for_invalid_char = re.search(
            patter_set, f"{local_part}{domain}").groupdict()

        if compile_for_invalid_char:
            raise ValueError(
                f"Invalid email address contain any of "
                f"prohibited char"
            )
        return email

    def get_access_token(self, apps):

        access_token: AccessToken = TokenFactory.create_access_token(
            {
                "user_data": {
                    "user_identifier": self.hash_identifier,
                    "apps": apps
                }
            })
        return access_token

    def get_refresh_token(self, apps):

        refresh_token: RefreshToken = TokenFactory.create_refresh_token(
            {
                "user_data": {
                    "user_identifier": self.hash_identifier,
                    "apps": apps
                }
            })
        return refresh_token

class ExternalLogin(CreatedUpdatedMixin, Base):

    __tablename__ = "external_logins"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    user_id = Column(Integer, ForeignKey("users.id"))
    configuration = Column(JSON, unique=False, nullable=True)

    users: Mapped["User"] = relationship(back_populates="external_logins")
