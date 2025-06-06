from fastapi import Request
from starlette.authentication import AuthenticationBackend, AuthenticationError, \
    SimpleUser

from inrastructure.security.exception.auth import TokenAuthException
from inrastructure.security.jwt.token import TokenFactory, AccessToken
from settings import APP_ID


class TokenAuthBackend(AuthenticationBackend):
    async def authenticate(self, request: Request):
        try:
            token = request.headers["Authorization"]
        except KeyError as exc:
            raise TokenAuthException(
                detail='Empty headers, fill token in Authorization key',
                status_code=400
            )

        validate, payload = AccessToken.validate(token, APP_ID)

        if not validate:
            raise TokenAuthException(
                detail='Invalid JWT Token.',
                status_code=400
            )
        return None, SimpleUser(username=payload['user_identifier'])