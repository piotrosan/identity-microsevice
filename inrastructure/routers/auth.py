from typing import Annotated, Any, Tuple

from fastapi import APIRouter
from fastapi import Body

from domain.auth.service import AuthService
from domain.auth.login_command import RegisterUserCommandFactory
from domain.user.service import UserService
from .request_models.request_auth import LoginData
from .request_models.request_user import RequestUserData, VerificationData, \
    RegistrationData
from .response_model.response_user import UserContext, ResponseRegisterUser, \
    ResponseUserSecurity
from ..database.sql.api.user import IdentityUserDBAPI
from ..database.sql.models import User

from ..security.jwt.token import AccessToken, RefreshToken

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

command = RegisterUserCommandFactory

@router.post("/login", response_model=ResponseUserSecurity)
def login(
        user_data: Annotated[
            LoginData, Body(embed=True)]
) -> Any:
    login_command = command.from_request_data(user_data)
    user, context_address = login_command()
    return ResponseUserSecurity(
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




@router.post("/token-verify", response_model=UserContext)
def token_verify(
        verification_data: Annotated[
            VerificationData, Body(embed=True)]
) -> Any :
    validate, payload = AuthService.token_verify(verification_data)
    return UserContext(
        validate=validate,
        payload=payload
    )


@router.post("/refresh-token", response_model=UserContext)
def refresh_token(
        verification_data: Annotated[
            VerificationData, Body(embed=True)]
):
    token, refresh_token = AuthService.refresh_token(verification_data)
    return UserContext(
        token=token.access_token,
        refresh_token=refresh_token.refresh_token
    )



# @router.put(
#     "/{item_id}",
#     tags=["custom"],
#     responses={403: {"description": "Operation forbidden"}},
# )
# async def update_item(item_id: str):
#     if item_id != "plumbus":
#         raise HTTPException(
#             status_code=403, detail="You can only update the item: plumbus"
#         )
#     return {"item_id": item_id, "name": "The great Plumbus"}