from typing import Dict, Annotated, Union, Any

import requests
import starlette

from fastapi import APIRouter, Depends, HTTPException
from fastapi import Body

from domain.auth import Auth
from domain.login_command_handler import RegisterUserCommandFactory
from .request_models.request_user import RequestUser, RegistrationData, \
    VerificationData
from domain.user_service import UserService
from .response_model.response_register import UserContext
from ..jwt.token import AccessToken, RefreshToken

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

command = RegisterUserCommandFactory

@router.post(
    "/register",
    response_model=Union[UserContext]
)
async def register(
        registration_data: Annotated[
            RegistrationData, Body(embed=True)]
) -> Any:
    user_api = UserService()
    try:
        return await user_api.register(registration_data)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Item not found {e}")


# @router.post("/login", response_model=UserContext)
# async def login(user_data: RequestUser):
#     l = command.from_request_data(user_data)
#     user_context = l()
#     return UserContext(**user_context)
#
#
# @router.post("/token-verify", response_model=UserContext)
# async def token_verify(
#         verification_data: Annotated[VerificationData, Body(embed=True)]
# ):
#     return  Auth.token_verify(verification_data)
#
#
# @router.post("/refresh-verify", response_model=UserContext)
# async def refresh_token(
#         verification_data: Annotated[VerificationData, Body(embed=True)]
# ):
#     return Auth.refresh_token(verification_data)


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