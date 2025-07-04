from typing import Annotated, Any, Tuple
from uuid import UUID

from fastapi import APIRouter
from fastapi import Body
from redis import Redis
from starlette.requests import Request

from domain.auth.service import AuthService
from domain.auth.login_command import RegisterUserCommandFactory
from domain.user.service import UserService
from inrastructure.cache.api.redis import RedisCache
from inrastructure.routers.request_models.request_auth import LoginData, \
    RegistrationData, RegistrationAPPData
from inrastructure.routers.request_models.request_user import RequestUserData, VerificationData
from inrastructure.routers.response_model.response_generic import \
    GenericResponse
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
            LoginData, Body(...)]
) -> ResponseRegisterUser:
    login_command = command.from_request_data(user_data)
    user, context_address, hash_identifier, register_app_list = login_command()
    return ResponseRegisterUser(
        access_token=user.get_access_token(register_app_list).access_token,
        refresh_token=user.get_refresh_token(register_app_list).refresh_token,
        context_address=context_address,
        hash_identifier=hash_identifier
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
        str,
        UUID
    ] = await user_api.register(registration_data)
    access_token = all_context[0]
    refresh_token = all_context[1]

    return ResponseRegisterUser(
        access_token=access_token.access_token,
        refresh_token=refresh_token.refresh_token,
        context_address=all_context[2],
        hash_identifier=all_context[3]
    )


@router.post(
    "/app_register",
    response_model=GenericResponse,
    status_code=200
)
async def app_register(
        registration_data: Annotated[
            RegistrationAPPData, Body(...)
        ]
) -> GenericResponse:
    r = RedisCache()
    r.set_app_registry(**registration_data.model_dump(mode='python'))
    return GenericResponse(message='App registered', timestamp='')


@router.post(
    "/app_unregister",
    response_model=GenericResponse,
    status_code=200
)
async def app_unregister(
        registration_data: Annotated[
            RegistrationAPPData, Body(...)
        ]
) -> GenericResponse:
    r = RedisCache()
    r.unset_app_registry(registration_data.app)
    return GenericResponse(message='App unregistered', timestamp='')


@router.post("/token-verify", response_model=ResponseUserContext)
def token_verify(
        verification_data: Annotated[
            VerificationData, Body(...)],
        request: Request
):
    validated, hash_identifier, email, permission_conf  = (
        AuthService.token_verify(verification_data)
    )
    return ResponseUserContext(
        validate=validated,
        permission=permission_conf,
        hash_identifier=hash_identifier
    )


@router.get("/token-validate", response_model=dict)
def token_validate(request: Request):
    return {
        'hash_identifier': request.user.hash_identifier
    }


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
