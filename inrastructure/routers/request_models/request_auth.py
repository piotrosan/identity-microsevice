from typing import List
from pydantic import BaseModel
from inrastructure.routers.request_models.request_user import RequestUserData


class RegistrationData(BaseModel):
    user: RequestUserData
    external_login: str
    apps: List[str] | None = None


class RegistrationAPPData(BaseModel):
    app: str
    name: str
    na_me: str


class LoginData(BaseModel):
    email: str
    password: str
