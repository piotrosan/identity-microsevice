import json
from typing import Tuple, List, Generator
from uuid import UUID

from inrastructure.cache.api.redis import RedisCache
from inrastructure.mail.mail import render_template
from inrastructure.mail.tools import send_mail
from domain.user.base_service import Service
from inrastructure.database.sql.models import User, ExternalLogin, \
    UserPermissions
from inrastructure.database.sql.api.user import IdentityUserDBAPI
from inrastructure.routers.request_models.request_auth import RegistrationData
from inrastructure.routers.request_models.request_user import UpdateUserData
from inrastructure.security.jwt.token import TokenFactory, AccessToken, \
    RefreshToken
from inrastructure.settings.context_app import settings
from inrastructure.mail.link_tools import generate_activation_link
from settings import root_path


class UserService(Service):

    model = User

    def __init__(self, infrastructure_db: IdentityUserDBAPI):
        self.infrastructure_db = infrastructure_db
        super().__init__()

    def _add_user(self, registration_data: RegistrationData) -> User:
        result = self.infrastructure_db.insert_user_with_external_login(
            registration_data.user.model_dump(mode="python"),
            json.loads(registration_data.external_login),
            json.loads(registration_data.user_permission)
        )
        return result[0]

    def _set_cache_context(self, user: User) -> str:
        cache_context = RedisCache()
        context_identifier = cache_context.set_context(user)
        return context_identifier

    async def register(
            self,
            registration_data: RegistrationData
    ) -> Tuple[AccessToken, RefreshToken, str]:
        user = self._add_user(registration_data)
        context_identifier = self._set_cache_context(user)

        access_token = TokenFactory.create_access_token({
            "user_data": {
                "user_identifier": user.hash_identifier,
                "apps": registration_data.apps
            }
        })
        refresh_token = TokenFactory.create_refresh_token({
            "user_data": {
                "user_identifier": user.hash_identifier,
                "apps": registration_data.apps
            }
        })
        await self._send_activation_link(user)
        return access_token, refresh_token, context_identifier

    async def _send_activation_link(self, user: User):
        template_root = f"{root_path}/domain/template/"
        activation_template = "activation_link.html"
        data = {
            'activation_link': generate_activation_link(
                user, settings.host, settings.http_secure)
        }
        body = render_template(template_root, activation_template, data)
        await send_mail("Activate user", body, [user.email])

    def get_user_detail(self, user_hash: UUID):
        user_combo_data = self.infrastructure_db.get_all_context_for_user_hash(
            user_hash
        )
        # ToDO after fill all data
        return user_combo_data

    def get_user_detail_for_login_data(
            self,
            email: str,
            password: str
    ) -> User:
        gen_user: Generator[User] = self.infrastructure_db.get_all_context_for_user_email_password(
            email,
            password
        )
        users: list[User] = next(gen_user)
        return users[0]

    def update_user_detail(self, user_hash: UUID, data: UpdateUserData):
        # user = self.infrastructure_db.get_all_context_for_user_hash(
        #     user_hash
        # )
        # {setattr(user, key, value) for key, value in data.items()}
        # self.infrastructure_db.
        # return user_combo_data
        pass