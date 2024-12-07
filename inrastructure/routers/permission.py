from functools import lru_cache
from typing import Any, Annotated
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi import APIRouter

from inrastructure.routers.request_models.request_user import (
    PermissionRequestData)
from inrastructure.routers.response_model.response_register import \
    PermissionResponseData

router = APIRouter(
    prefix="/permission",
    tags=["permission"],
    responses={404: {"description": "Not found"}},
)


@lru_cache
async def get_user(token: Annotated[str, Header()]):
    if token != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return token



@router.post("/", response_model=PermissionResponseData)
async def add_permission(
        permission_data: PermissionRequestData,
        token: Annotated[str, Depends(get_user)]
) -> Any:
    return {}