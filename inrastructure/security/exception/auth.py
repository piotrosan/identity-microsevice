from fastapi import HTTPException


class TokenAuthException(HTTPException):
    pass
