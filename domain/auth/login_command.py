from asyncio import Task
from typing import Tuple, List
from uuid import UUID

from domain.exception.http.auth import LoginHttpException
from domain.user.service import UserService
from inrastructure.cache.api.redis import RedisCache
from inrastructure.database.sql.api.user import IdentityUserDBAPI
from inrastructure.database.sql.models import User
from inrastructure.routers.request_models.request_auth import LoginData
from inrastructure.validators.user import UserDataValidator
from inrastructure.webhooks.permissions import UserPermission, \
    PermissionOperation


class Login:
    command = None

    def __init__(self, command: LoginData):
        self.command = command

    def _step_get_user(self) -> User:
        iu_db_api = IdentityUserDBAPI()
        us = UserService(iu_db_api)
        user: User = us.get_user_detail_for_login_data(
            self.command.email,
            self.command.password
        )
        return user

    def _step_get_user_permissions(self, user) -> List[dict]:
        ups: List[dict] = UserPermission.get_result_operation(
            PermissionOperation.GET,
            user
        )
        return ups

    def _step_set_context(self, user, ups) -> str:
        rc = RedisCache()
        return rc.set_context(user, ups)


    def _login(self) -> Tuple[User, str, UUID]:
        if not self.command:
            raise LoginHttpException(status_code=400)

        user = self._step_get_user()
        ups = self._step_get_user_permissions(user)
        context_address = self._step_set_context(user, ups)

        return (
                user,
                context_address,
                user.hash_identifier,
            )

    def __call__(self) -> Tuple[User, str, UUID, List[str]]:
        return self._login()

class RegisterUserCommandFactory:
    user_data_validator = UserDataValidator

    @classmethod
    def from_request_data(cls, user_data: LoginData) -> Login:
        return Login(user_data)
