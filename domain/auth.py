from typing import Tuple

from inrastructure.jwt.token import Token, RefreshToken, TokenFactory, \
    AccessToken
from inrastructure.routers.request_models.request_user import (
    RequestUser, LoginRequest, VerificationData
)

from inrastructure.routers.response_model.response_register import UserContext


class Auth:

    @classmethod
    def token_verify(cls, verification_data: VerificationData) -> Tuple[bool, dict]:
        return Token.validate(
            verification_data.user_context.token,
            verification_data.app
        )


    @classmethod
    def refresh_token(cls, verification_data: VerificationData) -> UserContext:
        token: AccessToken = TokenFactory.access_token_from_refresh_token(
            verification_data.user_context.refresh_token)
        refresh_token: RefreshToken = TokenFactory.recreate_refresh_token(
            verification_data.user_context.refresh_token)

        user_context = UserContext(
            token=token.access_token,
            refresh_token=refresh_token.refresh_token
        )
        return user_context
