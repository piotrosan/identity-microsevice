from sqlalchemy import (
    ForeignKey,
)

from sqlalchemy.orm import mapped_column, relationship, Mapped

from inrastructure.database.models.user import User
from inrastructure.database.models.permissions import UserGroup
from inrastructure.database.models.base import Base

class AssociationUserUserGroup(Base):
    __tablename__ = "association_user_user_group"
    __table_args__ = {'extend_existing': True}

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), primary_key=True)
    group_id: Mapped[int] = mapped_column(
        ForeignKey("user_groups.id"), primary_key=True
    )
    user: Mapped["User"] = relationship(UserGroup)
    user_group: Mapped["UserGroup"] = relationship(User)
