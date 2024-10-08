from inrastructure.routers.request_models.request_user import Token, \
    RequestUser, LoginRequest


class Auth:

    def token_verify(self, token: Token) -> bool:
        pass

    def login(self, login_user_request: LoginRequest):
        pass