from typing import List
from pydantic import BaseModel
from inrastructure.routers.request_models.request_user import RequestUserData


class RegistrationData(BaseModel):
    user: RequestUserData
    external_login: str
    user_permission: str
    apps: List[str]


class LoginData(BaseModel):
    email: str
    password: str
