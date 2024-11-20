from importlib import reload
from typing import Sequence, Iterable, List, cast
from uuid import UUID

from typing_extensions import Any

from . import session
from sqlalchemy import Select, Update, select, Row, and_, text, String

from .helpers import generate_user_identifier
from .models.permissions import UserGroup
from .. import sql_database as reload_session
from .models.user import User, ExternalLogin


class UserDatabaseAPI:

    def reload_session(self):
        reload(reload_session)

    def query_statement(self, select_query: Select[Any]) -> Row[Any]:
        with session as s:
            for row in s.execute(select_query):
                yield row

    def insert_objects(self, objects: Iterable[User]) -> Iterable[User]:
        with session as s:
            s.add_all(objects)
            s.commit()
        return objects

    def _update_statement(self, upd: Update[Any]):
        with session as s:
            s.execute(upd).scalar()
            s.commit()


class IdentityUserDBAPI:

    def __init__(self, db_interface: UserDatabaseAPI):
        self.db = db_interface

    def insert_user_with_external_login(
            self, user_data: dict, external_login_data: dict) -> Iterable[User]:
        """
        :param external_login_data:
        :param user_data:
        :return: list of id of created models
        """
        user = User(**user_data)
        user.set_hash_identifier(user.email)
        external_login_data = ExternalLogin(**external_login_data)
        user.external_login = external_login_data
        return self.db.insert_objects([user])

    def _select_all_user(
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


    def _select_user_from_hash(self, user_hash: UUID):
        return select(User).where(
            cast(
                "ColumnElement[bool]",
                User.hash_identifier == str(user_hash)
            )
        )

    def query_all_users_with_external_login_generator(
            self,
            column: List[str] = None,
            order: List[str] = None
    ) -> Row[Any]:
        return self.db.query_statement(
            self._select_all_user(column, order)
        )

    def query_user_generator(
            self,
            user_hash: UUID
    ) -> Row[Any]:
        return self.db.query_statement(
            self._select_user_from_hash(user_hash)
        )

    def raw_query_user(
            self,
            select_query: Select[Any],
    ) -> Sequence[Row]:
        return self._query_statement(
            self.db.query_statement(select_query)
        ).all()

    def raw_query_user_generator(
            self,
            select_query: Select[Any],
    ) -> Row[Any]:
        return self._query_statement(
            self.db.query_statement(select_query)
        )
