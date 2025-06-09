import logging
from typing import Sequence, Iterable, List, cast, Tuple, Generator, Iterator
from uuid import UUID

from typing_extensions import Any

from sqlalchemy import Select, Update, select, Row, and_, text, String
from sqlalchemy import exc
from inrastructure.database.sql.api.engine import DBEngineAbstract, DBEngine
from inrastructure.database.sql.api.sql.get import SQLSelect
from inrastructure.database.sql.exception.user import HttpUserDBException
from inrastructure.database.sql.models import UserPermissions
from inrastructure.database.sql.models.user import User, ExternalLogin

logger = logging.getLogger("root")


class CreateUserDBAPI(DBEngineAbstract):
    def insert_user_with_external_login(
            self,
            user_data: dict,
            external_login_data: dict,
            user_permission: dict
    ) -> Iterable[User]:
        """
        :param external_login_data:
        :param user_data:
        :return: list of id of created models
        """
        try:
            user = User(**user_data)
            user.set_hash_identifier(user.email)
            external_login_data = ExternalLogin(**external_login_data)
            user.external_logins = external_login_data
            user_permission = UserPermissions(**user_permission)
            user.user_permissions = [user_permission]
            return self.insert_objects([user])
        except exc.SQLAlchemyError as e:
            logger.critical(f"Problem wile insert user {user_data} -> {e}")
            raise HttpUserDBException(
                detail="Can not insert user",
                status_code=400
            )


class GetUserDBAPI(DBEngineAbstract, SQLSelect):

    def query_all_users_with_external_login_generator(
            self,
            column: List[str] = None,
            order: List[str] = None
    ) -> Iterator[Any]:
        try:
            return self.query_statement(
                self._select_all_user_sql(column, order)
            )
        except exc.SQLAlchemyError as e:
            logger.critical("Problem wile select all users")
            raise HttpUserDBException(
                detail="Can not select users",
                status_code=400
            )

    def query_user_generator(
            self,
            user_hash: UUID
    ) -> Iterator[Any]:
        try:
            return self.query_statement(
                self._select_user_from_hash_sql(user_hash)
            )
        except exc.SQLAlchemyError as e:
            logger.critical(f"Problem wile select user {user_hash} -> {e}")
            raise HttpUserDBException(
                detail=f"Can not select user {user_hash}",
                status_code=400
            )

    def raw_query_user(
            self,
            select_query: Select[Any],
    ) -> Sequence[Any]:
        try:
            return list(self.query_statement(select_query))
        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile select user from "
                f"custom select statement -> {e}"
            )
            raise HttpUserDBException(
                detail="Can not select user",
                status_code=400
            )

    def raw_query_user_generator(
            self,
            select_query: Select[Any],
    ) -> Iterator[Any]:
        try:
            return self.query_statement(select_query)

        except exc.SQLAlchemyError as e:
            logger.critical(
                f"Problem wile select user from "
                f"custom select statement -> {e}"
            )
            raise HttpUserDBException(
                detail="Can not select user",
                status_code=400
            )

    def get_all_context_for_user_hash(
            self,
            user_hash: UUID
    ) -> Iterator[Any]:
        try:
            return self.query_statement(
                self._select_all_data_user_from_hash_sql(
                    user_hash)
            )
        except exc.SQLAlchemyError as e:
            logger.critical("Problem wile select all users")
            raise HttpUserDBException(
                detail=f"Can not select user {e}",
                status_code=400
            )

    def get_all_context_for_user_email_password(
            self,
            email: str,
            password: str
    ) -> Iterator[Any]:
        try:
            return self.query_statement(
                self._select_all_data_user_from_password_email_sql(
                    email,
                    password
                )
            )
        except exc.SQLAlchemyError as e:
            logger.critical("Problem wile select all users")
            raise HttpUserDBException(
                detail=f"Can not select user {e}",
                status_code=400
            )


class IdentityUserDBAPI(
    CreateUserDBAPI,
    GetUserDBAPI,
    DBEngine
):
    pass