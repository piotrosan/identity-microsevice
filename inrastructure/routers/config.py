from fastapi import APIRouter, Request

from inrastructure.cache.api.redis import RedisCache

router = APIRouter(
    prefix="/config",
    tags=["config"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def configuration(request: Request) -> dict:

    rc = RedisCache()
    apps = rc.get_app_registry()

    return {
        'apps': apps
    }
