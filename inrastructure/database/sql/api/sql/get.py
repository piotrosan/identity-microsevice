import logging
from typing import Sequence, Iterable, List, cast, Tuple, Generator
from uuid import UUID

from sqlalchemy import Select, Update, select, Row, and_, text, String
from sqlalchemy.orm import contains_eager

from inrastructure.database.sql.models.user import User, ExternalLogin

logger = logging.getLogger("root")

class SQLSelect:

    def _select_all_user_sql(
            self,
            column: List[str] = None,
            order: List[str] = None
    ):
        tmp_select = select(User)

        if column:
            tmp_select.column(*[text(col) for col in column])

        tmp_select.join_from(
            ExternalLogin,
            User
        )
        if order:
            tmp_select.order_by(*[text(col) for col in order])

        return tmp_select

    def _select_all_data_user_from_hash_sql(self, user_hash: UUID):
        return (
            select(User)
            .join(User.external_logins)
            .join(User.user_permissions)
            .where(
                cast(
                    "ColumnElement[bool]",
                    User.hash_identifier == str(user_hash)
                )
            )
            .options(contains_eager(User.user_permissions))
            .options(contains_eager(User.external_logins))
        )

    def _select_user_from_hash_sql(self, user_hash: UUID):
        return select(User).where(
            cast(
                "ColumnElement[bool]",
                User.hash_identifier == str(user_hash)
            )
        )


    def _select_all_data_user_from_password_email_sql(
            self,
            email: str,
            password: str
    ):

        return (
            select(User)
            .join(User.external_logins)
            .join(User.user_permissions)
            .where(
                and_(
                    cast(
                        "ColumnElement[bool]",
                        User.email == email
                    ),
                    cast(
                        "ColumnElement[bool]",
                        User.password == password
                    ),
                )
            )
            .options(contains_eager(User.user_permissions))
            .options(contains_eager(User.external_logins))
        )
