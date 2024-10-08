from fastapi import FastAPI
from inrastructure.routers import auth, users
app = FastAPI()


app.include_router(auth.router)
app.include_router(users.router)
# app.include_router(
#     admin.router,
#
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )