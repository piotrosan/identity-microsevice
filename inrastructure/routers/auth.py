from typing import Dict, Annotated

import requests

from fastapi import APIRouter, Depends, HTTPException
from fastapi import Body

from domain.auth import Auth
from domain.login_command_handler import RegisterUserCommandFactory
from .request_models.request_user import RequestUser, Token, RegistrationData, \
    VerificationData
from domain.users import Users
from .response_model.ResponseRegister import UserContext


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

command = RegisterUserCommandFactory

@router.post("/register", response_model=Dict)
async def register(
        registration_data: Annotated[
            RegistrationData, Body(embed=True)]
) -> Dict:
    users_ids = Users.add_user(registration_data)
    if not users_ids:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "User(s) was/were add"}


@router.post("/login", response_model=UserContext)
async def login(user_data: RequestUser):
    login = command.from_request_data(user_data)
    user_context = login()
    return UserContext(**user_context)



@router.post("/token-verify", response_model=UserContext)
async def token_verify(
        verification_data: Annotated[VerificationData, Body(embed=True)]
):
    return  Auth.token_verify(verification_data)


@router.post("/refresh-verify", response_model=UserContext)
async def refresh_token(
        verification_data: Annotated[VerificationData, Body(embed=True)]
):


    return


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