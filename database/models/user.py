from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Text,
    BOOLEAN,
    ForeignKey,
    UniqueConstraint
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import engine
from database.models.base import Base


class User(Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=True)
    age_range = Column(String(10), unique=False, nullable=True)
    sector = Column(String(20), unique=False, nullable=True)
    something_about_me = Column(Text, unique=False, nullable=True)
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


class ExternalLogin(Base):

    __tablename__ = "external_login"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    user_id = Column(Integer, ForeignKey("user.id"))
    gmail = Column(BOOLEAN)
    facebook = Column(BOOLEAN)
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    user = relationship("User", backref="external_login")


Base.metadata.create_all(engine)
