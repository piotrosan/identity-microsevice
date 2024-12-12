from typing import Dict, Annotated, Union, Any


from fastapi import APIRouter, Depends
from fastapi import Body

from domain.auth import Auth
from domain.login_command_handler import RegisterUserCommandFactory
from .request_models.request_user import RequestUser, RegistrationData, \
    VerificationData
from domain.user_service import UserService
from .response_model.response_register import UserContext

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
            RegistrationData, Body(...)]
) -> Any:
    user_api = UserService()
    return await user_api.register(registration_data)


@router.post("/login", response_model=UserContext)
async def login(user_data: Annotated[RequestUser, Body(embed=True)]):
    login_command = command.from_request_data(user_data)
    user_context = login_command()
    return UserContext(**user_context)


@router.post("/token-verify", response_model=UserContext)
async def token_verify(
        verification_data: Annotated[VerificationData, Body(embed=True)]
) -> Any :
    validate, payload = Auth.token_verify(verification_data)
    return UserContext(
        validate=validate,
        hash_identifier=payload["hash_identifier"]
    )



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