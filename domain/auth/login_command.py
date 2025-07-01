from typing import Tuple, List
from uuid import UUID

from domain.exception.http.auth import LoginHttpException
from domain.user.service import UserService
from inrastructure.cache.api.redis import RedisCache
from inrastructure.database.sql.api.user import IdentityUserDBAPI
from inrastructure.database.sql.models import User
from inrastructure.routers.request_models.request_auth import LoginData
from inrastructure.validators.user import UserDataValidator


class Login:
    command = None

    def __init__(self, command: LoginData):
        self.command = command

    def _login(self) -> Tuple[User, str, UUID, List[str]]:
        if not self.command:
            raise LoginHttpException(status_code=400)
        iu_db_api = IdentityUserDBAPI()
        us = UserService(iu_db_api)
        user = us.get_user_detail_for_login_data(
            self.command.email,
            self.command.password
        )
        rc = RedisCache()
        context_address = rc.set_context(user)
        register_apps: List[List[dict]] = rc.get_app_registry()


        return (
            user,
            context_address,
            user.hash_identifier,
            list(register_apps[0][0])
        )

    def __call__(self) -> Tuple[User, str, UUID, List[str]]:
        return self._login()

class RegisterUserCommandFactory:
    user_data_validator = UserDataValidator

    @classmethod
    def from_request_data(cls, user_data: LoginData) -> Login:
        return Login(user_data)
