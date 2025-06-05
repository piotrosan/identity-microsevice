import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI
from inrastructure.routers import auth, users


app = FastAPI()


@asynccontextmanager
async def set_context():
    pass

# @app.middleware("http")
# async def set_base_url(request: Request, call_next):
#     if not settings.base_link:
#         url = request.url
#         settings.base_link = request.base_url
#         settings.host = url.hostname
#         settings.http_secure = True if url.scheme == 'https' else False
#     response = await call_next(request)
#     return response


app.include_router(auth.router)
app.include_router(users.router)
# app.include_router(
#     admin.router,
#
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )

if __name__ == "__main__":
    # Start uvicorn
    uvicorn.run(app, host="localhost", port=8001)