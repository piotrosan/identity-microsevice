from sqlalchemy import (
    ForeignKey,
)

from sqlalchemy.orm import mapped_column, relationship, Mapped

from inrastructure.database.models.user import User
from inrastructure.database.models.permissions import UserGroup
from inrastructure.database.models import Base

class AssociationUserUserGroup(Base):
    __tablename__ = "association_user_user_group"
    __table_args__ = {'extend_existing': True}

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), primary_key=True)
    group_id: Mapped[int] = mapped_column(
        ForeignKey("user_group.id"), primary_key=True
    )
    user: Mapped["User"] = relationship(back_populates="parents")
    user_group: Mapped["UserGroup"] = relationship(back_populates="children")
