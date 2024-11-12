from inrastructure.jwt.token import Token, RefreshToken
from inrastructure.routers.request_models.request_user import (
    RequestUser, LoginRequest, VerificationData
)

from inrastructure.routers.response_model.response_register import UserContext


class Auth:

    @classmethod
    def token_verify(cls, verification_data: VerificationData) -> bool:
        token = Token()
        return token.validate(
            verification_data.user_context.token,
            verification_data.app
        )

    @classmethod
    def refresh_token(cls, verification_data: VerificationData) -> UserContext:
        refresh_token = RefreshToken()
        access_token = refresh_token.get_access_token_obj(
            verification_data.user_context.refresh_token
        )
        refresh_token.set_user_data({
            "user_identifier": access_token.user_identifier
        })
        verification_data.user_context.token = access_token.get_access_token()
        verification_data.user_context.refresh_token = refresh_token.get_refresh_token()
        return verification_data.user_context
