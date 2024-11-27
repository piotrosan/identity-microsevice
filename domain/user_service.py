from uuid import UUID
import logging
import jwt
from typing import Any, List, Iterable

from sqlalchemy import Result


from inrastructure.database.sql.models.user import User
from inrastructure.database.sql.user_database_api import (
    UserDatabaseAPI,
    IdentityUserDBAPI,
)
from inrastructure.jwt.token import AccessToken, RefreshToken
from inrastructure.routers.request_models.request_user import RegistrationData
from inrastructure.routers.response_model.response_register import UserContext

logger = logging.getLogger("root")

class UserService:

    uda = IdentityUserDBAPI(UserDatabaseAPI())
    model = User

    def add_user(self, registration_data: RegistrationData) -> User:
        result = self.uda.insert_user_with_external_login(
            registration_data.user_data.model_dump(mode="python"),
            registration_data.external_login_data.model_dump(mode="python")
        )
        return result[0]

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
        # ToDo check what i must return
        return self.uda.query_user_generator(user_hash)

    def list_user(self):
        pass