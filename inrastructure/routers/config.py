from fastapi import APIRouter
from starlette.requests import Request

router = APIRouter(
    prefix="/config",
    tags=["config"],
    responses={404: {"description": "Not found"}},
)



@router.get("/")
def configuration(request: Request) -> dict:
    return {
        'apps': ['test-knowledge', 'test-grammar']
    }
