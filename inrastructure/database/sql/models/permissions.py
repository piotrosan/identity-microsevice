from sqlalchemy import (
    Column,
    Integer,
    String,
    JSON, ForeignKey, UniqueConstraint
)

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

from inrastructure.database.sql.models.base import Base
from inrastructure.database.sql.models.mixins import CreatedUpdatedMixin


class UserPermissions(CreatedUpdatedMixin, Base):

    __tablename__ = "user_permissions"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "app",
            name="unique_user_id_app_constraint"
        ),
    )

    id = Column(Integer, primary_key=True, autoincrement="auto")

    user_id = Column(Integer, ForeignKey("users.id"))
    app = Column(String(100))

    configuration = Column(JSON, unique=False, nullable=True)

    users: Mapped["User"] = relationship(back_populates="user_permissions")