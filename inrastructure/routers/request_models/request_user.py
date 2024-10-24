from pydantic import BaseModel


class RequestUser(BaseModel):
    email: str
    password: str | None = None
    age_range: str | None = None
    sector: str | None = None
    something_about_me: str | None = None


class LoginRequest(BaseModel):
    gmail: bool | None = None
    facebook: bool | None = None
    email: str | None = None
    password: str | None = None


class RegistrationData:
    user_data: RequestUser
    external_login_data: LoginRequest


class Token(BaseModel):
    token: str


class RegistrationDexcata:
    pass