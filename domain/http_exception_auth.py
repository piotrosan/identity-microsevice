from fastapi import HTTPException


class RegisterHttpException(HTTPException):
    status_code = 400
    detail = "Register failed"

class TokenHttpException(HTTPException):
    status_code = 400
    detail = "Invalid token"