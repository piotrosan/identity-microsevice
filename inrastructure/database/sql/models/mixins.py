from sqlalchemy import (
    Column,
    DateTime,
)

from sqlalchemy.sql import func

class CreatedUpdatedMixin:
    create_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
