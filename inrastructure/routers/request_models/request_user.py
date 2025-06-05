from pydantic import BaseModel


class RequestUser(BaseModel):
    email: str
    password: str | None = None
    age_range: str | None = None
    additional_info: str | None = None


class RegistrationData(BaseModel):
    user: RequestUser
    external_login: str
    user_permission: str


class VerificationData(BaseModel):
    token: str
    app: str


class PermissionRequestData:
    pass



