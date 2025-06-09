from typing import Tuple

from dns.dnssec import validate

from domain.user.service import UserService
from inrastructure.cache.api.redis import RedisCache
from inrastructure.database.sql.api.user import IdentityUserDBAPI
from inrastructure.database.sql.models import User
from inrastructure.security.jwt.token import Token, RefreshToken, TokenFactory, \
    AccessToken
from inrastructure.routers.request_models.request_user import (
    VerificationData
)


class AuthService:

    @classmethod
    def token_verify(cls, verification_data: VerificationData) -> Tuple[
        bool, str, str, dict]:

        # check correct token
        validated, payload = Token.validate(
            verification_data.user_context.token,
            verification_data.app
        )

        # check exist user
        idb = IdentityUserDBAPI()
        us = UserService(idb)
        user: User = us.get_user_detail(payload['user_identifier'])

        # get session
        r = RedisCache()
        context_address: str
        email: str
        permission_conf: dict
        context_address, email, permission_conf = r.get_context(user)

        return validated, user.hash_identifier , email, permission_conf


    @classmethod
    def refresh_token(cls, verification_data: VerificationData) -> Tuple[
        AccessToken, RefreshToken]:
        token: AccessToken = TokenFactory.access_token_from_refresh_token(
            verification_data.token)
        refresh_token: RefreshToken = TokenFactory.recreate_refresh_token(
            verification_data.user_context.refresh_token)
        return token, refresh_token
