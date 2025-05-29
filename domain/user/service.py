from typing import Tuple
from uuid import UUID

from inrastructure.mail.mail import render_template
from inrastructure.mail.tools import send_mail
from domain.user.base_service import Service
from inrastructure.database.sql.models import User
from inrastructure.database.sql.api.user import IdentityUserDBAPI
from inrastructure.routers.request_models.request_user import RegistrationData
from inrastructure.security.jwt.token import TokenFactory
from inrastructure.settings.context_app import settings
from tools.link_tools import generate_activation_link


class UserService(Service):

    model = User

    def __init___(self, infrastructure_db: IdentityUserDBAPI):
        self.infrastructure_db = infrastructure_db
        super().__init__()


    def add_user(self, registration_data: RegistrationData) -> User:
        result = self.infrastructure_db.insert_user_with_external_login(
            registration_data.user_data.model_dump(mode="python"),
            registration_data.external_login_data.model_dump(mode="python")
        )
        return result[0]


    async def register(
            self,
            registration_data: RegistrationData
    ) -> Tuple[str, str, str]:
        user = self.add_user(registration_data)
        access_token = TokenFactory.create_access_token({
            "user_data": {
                "user_identifier": user.hash_identifier
            }
        })
        refresh_token = TokenFactory.create_refresh_token({
            "user_data": {
                "user_identifier": user.hash_identifier
            }
        })
        access_token = access_token.access_token
        refresh_token= refresh_token.refresh_token

        await self._send_activation_link(user)
        return access_token, refresh_token, user.hash_identifier


    async def _send_activation_link(self, user: User):
        template_root = "template/"
        activation_template = "activation_link.html"
        data = {
            'activation_link': generate_activation_link(
                user, settings.host, settings.http_secure)
        }
        body = render_template(template_root, activation_template, data)
        await send_mail("Activate user", body, [user.email])

    def get_get_user_detail(self, user_hash: UUID):
        user_combo_data = self.infrastructure_db.get_all_context_for_user(
            user_hash)
        # ToDO after fill all data
        return user_combo_data

    def list_users(self):
        pass