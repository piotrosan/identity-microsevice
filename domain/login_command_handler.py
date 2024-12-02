from inrastructure.routers.request_models.request_user import RequestUser, \
    LoginRequest
from inrastructure.validators.user_data_validator import UserDataValidator


class Login:
    command = None

    def __init__(self, command: LoginRequest):
        self.command = command

    def _login(self) -> dict:
        pass

    def __call__(self) -> dict:
        try:
            return self._login()
        except Exception as e:
            #ToDo log
            pass

class RegisterUserCommandFactory:
    user_data_validator = UserDataValidator

    @classmethod
    def from_request_data(cls, user_data: RequestUser) -> Login:
        validated_user = cls.user_data_validator.validate(user_data)
        return Login(validated_user)
