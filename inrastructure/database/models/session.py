from xmlrpc.client import Boolean

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
    Interval
)

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from inrastructure.database import engine
from inrastructure.database.models import Base


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    duration = Column(Interval, nullable=False)
    hs_key = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    closed = Column(Boolean, nullable=False)
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    user: Mapped["User"] = relationship("User", back_populates="sessions")