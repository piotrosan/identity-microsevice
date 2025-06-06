from typing import List
from uuid import UUID

from pydantic import BaseModel

from inrastructure.database.sql.models.user import AgeRange


class ResponseUserData(BaseModel):
    email: str
    password: str | None = None
    age_range: AgeRange | None = None
    sector: str | None = None
    something_about_me: str | None = None


class ResponseRegisterUser(BaseModel):
    refresh_token: str
    access_token: str
    context_address: str


class ResponseUserSecurity(ResponseRegisterUser):
    pass


class DetailUserContext(BaseModel):
    user_groups: List[str]
    user_roles: List[str]
    user_hash: UUID


class PermissionResponseData:
    pass