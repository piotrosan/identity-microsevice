import abc
from importlib import reload
from typing import Iterable, Generator, Iterator, Any

from inrastructure.database.sql import session
from sqlalchemy import Select, Update
import inrastructure.database.sql as reload_session
from inrastructure.database.sql.api.pagination import Pagination
from inrastructure.database.sql.models import Base


class DBEngineAbstract(abc.ABC):
    def reload_session(self):
        raise NotImplemented()

    def query_statement(
            self,
            select_query: Select[Any],
    ) -> Iterator[Any]:
        raise NotImplemented()

    def insert_objects(
            self,
            objects: Iterable[Any]
    ) -> Iterable[Any]:
        raise NotImplemented()

    def _update_statement(self, upd: Update[Any]):
        raise NotImplemented()


class DBEngine(DBEngineAbstract):

    def reload_session(self):
        reload(reload_session)

    def query_statement(
            self,
            select_query: Select[Any],
            model: type[Base] = None,
            page: int = None
    ) -> Iterator[Any]:
        if page:
            pagination = Pagination(select_query, model)
            select_query = pagination.get_page(page)

        with session as s:
            for row in s.execute(select_query).unique():
                yield row


    def insert_objects(self, objects: Iterable[Any]) -> Iterable[Any]:
        with session as s:
            s.add_all(objects)
            s.commit()
        return objects

    def _update_statement(self, upd: Update[Any]):
        with session as s:
            s.execute(upd).scalar()
            s.commit()
