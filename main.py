import uvicorn

from fastapi import FastAPI, Depends
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware

from inrastructure.routers import auth, users, logging
from inrastructure.security.middleware.auth import TokenAuthBackend
from settings import DOMAIN, PORT


middlewares = [
    Middleware(
        AuthenticationMiddleware,
        backend=TokenAuthBackend()
    ),
]
app = FastAPI(
    # middleware=middlewares
)
app.include_router(auth.router)
app.include_router(
    users.router,
    # dependencies=[Depends()]
)
app.include_router(
    logging.router,
    # dependencies=[Depends()]
)
if __name__ == "__main__":
    # Start uvicorn
    # https://stackoverflow.com/questions/69207474/enable-https-using-uvicorn
    uvicorn.run(
        app,
        host=DOMAIN,
        port=PORT
    )