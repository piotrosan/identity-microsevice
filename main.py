from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI, Depends
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware

import settings
from inrastructure.cache.api.redis import RedisCache
from inrastructure.routers import auth, users, logging, config
from inrastructure.security.middleware.auth import TokenAuthBackend
from settings import HOST, PORT, APP_ID, SSL_CERTFILE, SSL_KEYFILE

origins = [
    'http://localhost:3000',
]

middlewares = [
    Middleware(
        AuthenticationMiddleware,
        backend=TokenAuthBackend()
    ),
    Middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_headers=['*'],
        allow_methods=['*']
    ),
]

def register_app():
    rc = RedisCache()
    rc.set_app_registry(
        APP_ID,
        'Identity',
        'identity',
        settings.BASE_URL,
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Register app in cache
    register_app()
    yield
    # Unregistered while restart


app = FastAPI(
    lifespan=lifespan,
    middleware=middlewares
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
app.include_router(
    config.router,
    # dependencies=[Depends()]
)

if __name__ == "__main__":
    # Start uvicorn
    # https://stackoverflow.com/questions/69207474/enable-https-using-uvicorn
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        ssl_certfile=SSL_CERTFILE,
        ssl_keyfile=SSL_KEYFILE
    )