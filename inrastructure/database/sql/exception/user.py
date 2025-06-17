from fastapi import HTTPException


class HttpUserDBException(HTTPException):
    status_code = 400
    detail = "Problem with database operation"


class HttpUserModelException(HTTPException):
    status_code = 400
    detail = "Problem with database operation"



