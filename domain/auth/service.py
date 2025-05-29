from typing import Tuple

from inrastructure.security.jwt.token import Token, RefreshToken, TokenFactory, \
    AccessToken
from inrastructure.routers.request_models.request_user import (
    VerificationData
)


class AuthService:

    @classmethod
    def token_verify(cls, verification_data: VerificationData) -> Tuple[bool, dict]:
        return Token.validate(
            verification_data.user_context.token,
            verification_data.app
        )

    @classmethod
    def refresh_token(cls, verification_data: VerificationData) -> Tuple[
        AccessToken, RefreshToken]:
        token: AccessToken = TokenFactory.access_token_from_refresh_token(
            verification_data.token)
        refresh_token: RefreshToken = TokenFactory.recreate_refresh_token(
            verification_data.user_context.refresh_token)
        return token, refresh_token
