import cachetools
from fastapi import Request
from starlette.authentication import AuthenticationBackend

from domain.user.service import UserService
from inrastructure.database.sql.api.user import IdentityUserDBAPI
from inrastructure.database.sql.models import User
from inrastructure.logger_sys.settings.logger_conf import logger
from inrastructure.security.exception.auth import TokenAuthException
from inrastructure.security.jwt.token import AccessToken
from settings import APP_ID


class TokenAuthBackend(AuthenticationBackend):

    @cachetools.cached(
        cache=cachetools.TTLCache(
            maxsize=128,
            ttl=10 * 60
        )
    )
    def _get_user(self, user_identifier) -> User:
        iu_db = IdentityUserDBAPI()
        us = UserService(iu_db)
        return us.get_user_detail(user_identifier)

    async def authenticate(self, request: Request):
        try:
            token = request.headers["Authorization"]
        except KeyError as exc:
            logger.info(msg='Empty headers, fill token in Authorization key')
            return None, None # SimpleUser(username='Anonymous')

        validate, payload = AccessToken.validate(token, APP_ID)

        if not validate:
            raise TokenAuthException(
                detail='Invalid JWT Token.',
                status_code=400
            )
        user = self._get_user(payload['user_identifier'])
        return None, user