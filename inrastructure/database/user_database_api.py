from importlib import reload
from typing import Sequence, Iterable, List

from typing_extensions import Any

from . import session
from sqlalchemy import Select, Result, Update, select, Row, text

from .models.base import Base
from .. import database as reload_session
from .models.user import User, ExternalLogin
from sqlalchemy.sql import operators


class UserDatabaseAPI:

    def reload_session(self):
        reload(reload_session)

    def _build_select(
            self,
            model: Base,
            join_models: tuple = None,
            column: tuple = None,
            conditions: dict = None,
            order: tuple = None
    ) -> Select[Any]:
        statement = select(model)
        if column is not None:
            statement = statement.column(*column)
        if join_models is not None:
            statement = statement.join_from(
                *[text(join_model) for join_model in join_models]
            )
        if conditions is not None:
            statement = statement.where(
                operators.__getattribute__(
                    conditions['op']
                )(*conditions['where_conditions'])
            )
        if order is not None:
            statement = statement.order_by(*order)

        return statement

    def query_statement(
            self,
            model,
            join_models: tuple = None,
            column: tuple = None,
            conditions: dict = None,
            order: tuple = None
    ) -> Row[Any]:
        with session as s:
            for row in s.execute(
                    self._build_select(
                        model, join_models, conditions, column, order)):
                yield row

    def insert_objects(self, objects: Iterable[object]) -> List[int]:
        with session as s:
            res = s.bulk_save_objects(objects)
            s.commit()
        return res

    def _update_statement(self, upd: Update[Any]):
        with session as s:
            s.execute(upd).scalar()
            s.commit()


class IdentityUserDBAPI:

    def __init__(self, db_interface: UserDatabaseAPI):
        self.db = db_interface

    def insert_user_with_external_login(
            self, user_data: dict, external_login_data: dict) -> List[int]:
        """
        :param external_login_data:
        :param user_data:
        :return: list of id of created models
        """
        user = User(**user_data)
        external_login_data = ExternalLogin(**external_login_data)
        user.external_login = external_login_data
        return self.db.insert_objects([user])

    def query_all_users_with_external_login_generator(
            self,
            model: Base,
            join_models: tuple = None,
            column: tuple = None,
            conditions: dict = None,
            order: tuple = None
    ) -> Row[Any]:
        return self.db.query_statement(model, column, order)

    def query_all_user(
            self,
            model,
            column: tuple = None,
            order: tuple = None
    ) -> Sequence[Row]:
        return self._query_statement(
            self._build_select(model, column, order)
        ).all()

    def query_result(
            self,
            model,
            column: tuple = None,
            conditions: list = None,
            order: tuple = None
    ) -> Result[Any]:
        return self._query_statement(
            self._build_select(model, column, conditions, order))