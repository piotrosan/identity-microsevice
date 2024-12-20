from typing import List

from fastapi import APIRouter

from inrastructure.routers.request_models.request_user import RequestUser
from inrastructure.routers.response_model.response_register import ResponseUserData

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


# @router.get("/", response_model=List[ResponseUserData])
# async def get_users():
#     return {}
#
#
# @router.get("/{user_id}", response_model=ResponseUserData)
# async def get_user(user_id: str):
#     return {}
#
#

@router.put("/{user_id}", response_model=ResponseUserData)
async def modify_user(user_data: RequestUser, user_id: str):
    return {}





