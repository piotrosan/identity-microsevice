import logging
from typing import Annotated, Any, Tuple
from fastapi import APIRouter, Body
from starlette.requests import Request

from inrastructure.routers.request_models.request_logging import LoggingData

from inrastructure.logger_sys.settings.logger_conf import logger


router = APIRouter(
    prefix="/logging",
    tags=["logging"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async def logging(
        data: Annotated[
               LoggingData, Body(...)
        ],
        request: Request) -> dict:
    logger.log(
        level=data.level,
        msg=data.message,
        extra={'app': data.app}
    )
    return {'saved': True}





