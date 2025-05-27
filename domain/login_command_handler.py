from domain.http_exception_auth import LoginHttpException
from inrastructure.routers.request_models.request_user import RequestUser, \
    LoginRequest
from inrastructure.validators.user_data_validator import UserDataValidator
from inrastructure.security.jwt.token import TokenFactory, AccessToken


class Login:
    command = None

    def __init__(self, command: RequestUser):
        self.command = command

    def _login(self) -> AccessToken:
        if not self.command:
            raise LoginHttpException(status_code=400)
        return TokenFactory.create_access_token(
            self.command.model_dump()
        )

    def __call__(self) -> AccessToken:
        return self._login()

class RegisterUserCommandFactory:
    user_data_validator = UserDataValidator

    @classmethod
    def from_request_data(cls, user_data: RequestUser) -> Login:
        validated_user = cls.user_data_validator.validate(user_data)
        return Login(validated_user)
