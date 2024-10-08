from pydantic import BaseModel


class RequestUser(BaseModel):
    email: str
    password: str | None = None
    age_range: str | None = None
    sector: str | None = None
    something_about_me: str | None = None


class LoginRequest:
    gmail: bool | None = None
    facebook: bool | None = None
    email: str | None = None
    password: str | None = None


class Token(BaseModel):
    token: str
