from fastapi import HTTPException


class DifferentTokenHashException(HTTPException):
    pass


class TokenAudienceException(HTTPException):
    pass


class TokenDecoderException(HTTPException):
    pass

class TokenEncoderException(HTTPException):
    pass