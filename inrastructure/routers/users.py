from typing import Annotated, Any, Tuple

from fastapi import APIRouter, Body

from inrastructure.routers.response_model.response_user import ResponseUserData
from inrastructure.routers.request_models.request_user import (

    UpdateUserData
)
from domain.user.service import UserService
from inrastructure.database.sql.api.user import IdentityUserDBAPI
from inrastructure.cache.api.redis import RedisCache
from inrastructure.database.sql.models import User
from inrastructure.security.jwt.token import AccessToken, RefreshToken


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.put("/", response_model=ResponseUserData)
async def update_user(user_data: UpdateUserData, request: Request):
    ido = IdentityUserDBAPI()
    us = UserService(ido)
    us.get_user_detail()






