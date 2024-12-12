from fastapi import HTTPException


class UserHttpException(HTTPException):
    status_code = 400
    detail = "User created failed"