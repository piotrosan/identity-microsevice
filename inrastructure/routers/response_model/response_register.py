from uuid import UUID

from pydantic import BaseModel


class ResponseUserData(BaseModel):
    email: str
    password: str | None = None
    age_range: str | None = None
    sector: str | None = None
    something_about_me: str | None = None


class UserContext(BaseModel):
    refresh_token: str | None = None
    token: str