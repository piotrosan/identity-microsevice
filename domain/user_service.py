from uuid import UUID

from domain.http_exception_auth import TokenHttpException
from domain.http_exception_user import UserHttpException
from domain.mail import render_template
from domain.tools import send_mail
from inrastructure.database.sql.models.user import User
from inrastructure.database.sql.user_database_api import (
    UserDatabaseAPI,
    IdentityUserDBAPI,
)
from inrastructure.security.jwt.exceptions import DifferentTokenHashException, TokenAudienceException
from inrastructure.security.jwt.token import TokenFactory
from inrastructure.routers.request_models.request_user import RegistrationData
from inrastructure.routers.response_model.response_register import UserContext, \
    DetailUserContext
from inrastructure.settings.context_app import settings
from tools.link_tools import generate_activation_link


class UserService:

    uda = IdentityUserDBAPI(UserDatabaseAPI())
    model = User

    def add_user(self, registration_data: RegistrationData) -> User:
        try:
            result = self.uda.insert_user_with_external_login(
                registration_data.user_data.model_dump(mode="python"),
                registration_data.external_login_data.model_dump(mode="python")
            )
            return result[0]
        except ValueError as e:
            raise UserHttpException(detail=str(e), status_code=400)
        except IndexError as e:
            raise UserHttpException(
                detail="User hasn't been added", status_code=400)

    async def register(self, registration_data: RegistrationData) -> UserContext:
        # import ipdb;ipdb.set_trace()
        user = self.add_user(registration_data)
        try:
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
            access_token_encoded = access_token.access_token
            refresh_token_encoded = refresh_token.refresh_token
        except DifferentTokenHashException as e:
            raise TokenHttpException(detail=str(e), status_code=400)
        except TokenAudienceException as e:
            raise TokenHttpException(detail=str(e), status_code=400)
        except ValueError as e:
            raise TokenHttpException(detail=str(e), status_code=400)

        await self._send_activation_link(user)
        return UserContext(
            token=access_token_encoded,
            refresh_token=refresh_token_encoded,
            hash_identifier=user.hash_identifier
        )

    async def _send_activation_link(self, user: User):
        template_root = "template/"
        activation_template = "activation_link.html"
        data = {
            'activation_link': generate_activation_link(
                user, settings.host, settings.http_secure)
        }
        body = render_template(template_root, activation_template, data)
        await send_mail("Activate user", body, [user.email])

    def get_get_user_detail(self, user_hash: UUID) -> DetailUserContext:
        user_combo_data = self.uda.get_all_context_for_user(user_hash)
        # ToDO after fill all data
        return DetailUserContext(user_groups=['test'], user_roles=['test_role'])

    def list_users(self):
        pass