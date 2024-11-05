from sqlalchemy import (
    Column,
    DateTime,
    String,
)

from sqlalchemy.sql import func

from inrastructure.database.models import Base


class BlockedEmailDomain(Base):
    domain = Column(String(255), unique=False, nullable=True)
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())