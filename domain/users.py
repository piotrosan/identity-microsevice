from uuid import UUID

import jwt
from typing import Any, List, Iterable

from sqlalchemy import Result
from sqlalchemy import exc

from inrastructure.database.models.user import User
from inrastructure.database.user_database_api import UserDatabaseAPI, IdentityUserDBAPI
from inrastructure.routers.request_models.request_user import RegistrationData


class Users:

    uda = IdentityUserDBAPI(UserDatabaseAPI())
    model = User

    def add_user(self, registration_data: RegistrationData) -> Iterable[User]:
        try:
            return self.uda.insert_user_with_external_login(
                registration_data.user_data.model_dump(mode="python"),
                registration_data.external_login_data.model_dump(mode="python")
            )
        except exc.UnmappedInstanceError as e:
            # todo log exception
            return []


    def register(self, registration_data: RegistrationData):
        users = self.add_user(registration_data)

    def get_user_data(self, user_hash: UUID) -> User:
        return self.uda.query_user_generator(user_hash)._t

    def list_user(self):
        pass