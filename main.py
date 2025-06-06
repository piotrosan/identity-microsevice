import uvicorn

from fastapi import FastAPI, Depends
from inrastructure.routers import auth, users
from settings import DOMAIN, PORT

app = FastAPI()
app.include_router(auth.router)
app.include_router(
    users.router,
    dependencies=[Depends()]
)

if __name__ == "__main__":
    # Start uvicorn
    # https://stackoverflow.com/questions/69207474/enable-https-using-uvicorn
    uvicorn.run(
        app,
        host=DOMAIN,
        port=PORT
    )