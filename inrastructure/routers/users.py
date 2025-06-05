from typing import Annotated, Any, Tuple

from fastapi import APIRouter, Body

from inrastructure.routers.response_model.response_register import ResponseUserData
from inrastructure.routers.request_models.request_user import RequestUser, RegistrationData
from domain.user.service import UserService
from inrastructure.routers.response_model.response_register import UserContext
from inrastructure.database.sql.api.user import IdentityUserDBAPI
from inrastructure.cache.api.redis import RedisCache
from inrastructure.database.sql.models import User
from inrastructure.security.jwt.token import AccessToken, RefreshToken


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

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
    all_context: Tuple[
        AccessToken,
        RefreshToken,
        User
    ] = await user_api.register(registration_data)
    cache_context = RedisCache()
    cache_context.set_context(all_context)


@router.put("/{user_id}", response_model=ResponseUserData)
async def modify_user(user_data: RequestUser, user_id: str):
    return {}





