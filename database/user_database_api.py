from typing import Sequence, Any

from typing_extensions import Any

from . import session
from sqlalchemy import Select, Result, Insert, Update, select, Row, insert

from .models.base import Base


class UserDatabaseAPI:

    def _build_select(
            self,
            model: Base,
            join_models: tuple = None,
            column: tuple = None,
            conditions: list = None,
            order: tuple = None
    ) -> Select[Any]:
        if column is None:
            column = []
        if conditions is None:
            conditions = []
        if order is None:
            order = []

        if column:
            return select(*column).join_from(*join_models).where(
                *conditions
            ).order_by(*order)
        else:
            select(model).join_from(*join_models).where(
                *conditions
            ).order_by(*order)

    def _build_insert(self, model: Base) -> Insert:
        return insert(model).returning(model)

    def _query_statement(self, sel: Select[Any]) -> Result[Any]:
        with session as s:
            return s.execute(sel)

    def _insert_statement(self, ins: Insert[Any], data: list) -> Result[Any]:
        with session as s:
            res = s.execute(ins, data)
            s.commit()
        return res

    def update_statement(self, upd: Update[Any]) -> Result[Any]:
        with session as s:
            return s.execute(upd)

    def insert(self, model: Base, data: list) -> Sequence[Row[Any | Any]]:
        ins = self._build_insert(model)
        return self._insert_statement(ins, data).fetchall()

    def query_all_generator(
            self,
            model,
            column: tuple = None,
            conditions: list = None,
            order: tuple = None
    ) -> Row[Any]:
        s = self._build_select(model, column, conditions, order)
        for row in self._query_statement(s):
            yield row

    def query_all(
            self,
            model,
            column: tuple = None,
            conditions: list = None,
            order: tuple = None
    ) -> Sequence[Row]:
        return self._query_statement(
            self._build_select(model, column, conditions, order)).all()

