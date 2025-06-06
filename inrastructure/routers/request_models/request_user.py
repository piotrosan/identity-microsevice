from pydantic import BaseModel

from inrastructure.database.sql.models.user import AgeRange



class RequestUserData(BaseModel):
    email: str
    password: str | None = None
    age_range: AgeRange | None = None
    additional_info: str | None = None


class UpdateUserData(RequestUserData):
    pass


class UpdateExternalLoginData(BaseModel):
    user: str
    configuration: str


class UpdateUserPermission(BaseModel):
    user: str
    configuration: str





class VerificationData(BaseModel):
    token: str
    app: str


class PermissionRequestData:
    pass



