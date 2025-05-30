from typing import Annotated, Any, Tuple

from fastapi import APIRouter
from fastapi import Body

from domain.auth.service import AuthService
from domain.auth.login_command import RegisterUserCommandFactory
from .request_models.request_user import RequestUser, RegistrationData, \
    VerificationData
from domain.user.service import UserService
from .response_model.response_register import UserContext
from inrastructure.database.sql.api.user import IdentityUserDBAPI
from ..cache.api.cache import RedisCache
from ..database.sql.models import User
from ..security.jwt.token import AccessToken, RefreshToken

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

command = RegisterUserCommandFactory

@router.post(
    "/register",
    response_model=UserContext
)
async def register(
        registration_data: Annotated[
            RegistrationData, Body(...)
        ]
) -> Any:
    api_db = IdentityUserDBAPI()
    user_api = UserService(api_db)
    all_user_context: Tuple[AccessToken, RefreshToken, User] = await user_api.register(
        registration_data
    )
    cache_context = RedisCache()
    cache_context.set_context(all_user_context)
@router.post("/login", response_model=UserContext)
def login(
        user_data: Annotated[
            RequestUser, Body(embed=True)]
) -> Any:
    login_command = command.from_request_data(user_data)
    token: AccessToken = login_command()
    return UserContext(**{'token': token.access_token})


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