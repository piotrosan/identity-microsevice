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

from sqlalchemy.sql import func

from inrastructure.database.sql.models.base import Base


class BlockedEmailDomain(Base):
    __tablename__ = "blocked_email_domain"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    domain = Column(String(255), unique=False, nullable=True)
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())