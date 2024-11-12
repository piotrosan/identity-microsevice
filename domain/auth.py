from inrastructure.routers.request_models.request_user import Token, \
    RequestUser, LoginRequest, VerificationData

from inrastructure.jwt.token_mixins import JwtValidator
from inrastructure.routers.response_model.ResponseRegister import UserContext


class Auth:

    @staticmethod
    def token_verify(cls, verification_data: VerificationData) -> bool:
        jwt_cv = JwtValidator()
        return jwt_cv.validate(
            verification_data.user_context.token, verification_data.app
        )

    def refresh_token(self, verification_data: VerificationData) -> UserContext:
        jwt_validator = JwtValidator()
        token, refresh_token = jwt_validator.refresh_token(
            verification_data.user_context.refresh_token)

        verification_data.user_context.token = token
        verification_data.user_context.refresh_token = refresh_token
        return verification_data.user_context

    @staticmethod
    def login(cls, login_user_request: LoginRequest):
        pass