from sqlalchemy import (
    Column,
    Integer,
    String,
)

from inrastructure.database.sql.models.base import Base
from inrastructure.database.sql.models.mixins import CreatedUpdatedMixin


class BlockedEmailDomain(CreatedUpdatedMixin, Base):

    __tablename__ = "blocked_email_domain"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    domain = Column(String(255), unique=True, nullable=True)
    email = Column(String(255), unique=True, nullable=True)
