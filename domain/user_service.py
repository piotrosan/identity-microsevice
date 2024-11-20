from uuid import UUID

import jwt
from typing import Any, List, Iterable

from sqlalchemy import Result
from sqlalchemy import exc

from inrastructure.sql_database.models.user import User
from inrastructure.sql_database.user_database_api import UserDatabaseAPI, IdentityUserDBAPI
from inrastructure.jwt.token import AccessToken, RefreshToken
from inrastructure.routers.request_models.request_user import RegistrationData
from inrastructure.routers.response_model.response_register import UserContext


class UserService:

    uda = IdentityUserDBAPI(UserDatabaseAPI())
    model = User

    def add_user(self, registration_data: RegistrationData) -> User:
        try:
            return self.uda.insert_user_with_external_login(
                registration_data.user_data.model_dump(mode="python"),
                registration_data.external_login_data.model_dump(mode="python")
            )[0]
        except exc.UnmappedInstanceError as e:
            # todo log exception
            return []


    def register(self, registration_data: RegistrationData) -> UserContext:
        user = self.add_user(registration_data)

        access_token = AccessToken()
        access_token.set_user_data({
            "user_identifier": user.hash_identifier
        })
        refresh_token = RefreshToken()
        refresh_token.set_user_data({
            "user_identifier": user.hash_identifier
        })
        return UserContext(
        token=access_token.get_access_token(),
        refresh_token=refresh_token.get_refresh_token()
    )

    def get_user_data(self, user_hash: UUID) -> User:
        return self.uda.query_user_generator(user_hash)

    def list_user(self):
        pass