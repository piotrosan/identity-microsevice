from typing import Annotated, Any, Tuple

from fastapi import APIRouter
from fastapi import Body

from domain.auth.service import AuthService
from domain.auth.login_command import RegisterUserCommandFactory
from domain.user.service import UserService
from inrastructure.routers.request_models.request_auth import LoginData, RegistrationData
from inrastructure.routers.request_models.request_user import RequestUserData, VerificationData
from inrastructure.routers.response_model.response_user import (
    ResponseRegisterUser,
    ResponseUserContext, RefreshTokenResponse
)
from inrastructure.database.sql.api.user import IdentityUserDBAPI

from inrastructure.security.jwt.token import AccessToken, RefreshToken

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

command = RegisterUserCommandFactory

@router.post("/login", response_model=ResponseRegisterUser)
def login(
        user_data: Annotated[
            LoginData, Body(embed=True)]
) -> ResponseRegisterUser:
    login_command = command.from_request_data(user_data)
    user, context_address = login_command()
    return ResponseRegisterUser(
        access_token=user.get_access_token().access_token,
        refresh_token=user.get_refresh_token().refresh_token,
        context_address=context_address
    )


@router.post(
    "/register",
    response_model=ResponseRegisterUser
)
async def register(
        registration_data: Annotated[
            RegistrationData, Body(...)
        ]
) -> ResponseRegisterUser:
    api_db = IdentityUserDBAPI()
    user_api = UserService(api_db)
    all_context: Tuple[
        AccessToken,
        RefreshToken,
        str
    ] = await user_api.register(registration_data)
    access_token = all_context[0]
    refresh_token = all_context[1]

    return ResponseRegisterUser(
        access_token=access_token.access_token,
        refresh_token=refresh_token.refresh_token,
        context_address=all_context[2]
    )


@router.post("/token-verify", response_model=ResponseUserContext)
def token_verify(
        verification_data: Annotated[
            VerificationData, Body(embed=True)]
):
    validated, hash_identifier, email, permission_conf  = (
        AuthService.token_verify(verification_data)
    )
    return ResponseUserContext(
        validate=validated,
        permission=permission_conf,
        hash_identifier=hash_identifier
    )


@router.post("/refresh-token", response_model=RefreshTokenResponse)
def refresh_token(
        verification_data: Annotated[
            VerificationData, Body(embed=True)]
):
    token, refresh_token = AuthService.refresh_token(verification_data)
    return RefreshTokenResponse(
        token=token.access_token,
        refresh_token=refresh_token.refresh_token
    )
