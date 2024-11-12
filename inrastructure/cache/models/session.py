from pydantic import BaseModel
from datetime import timedelta


class Session(BaseModel):

    duration: timedelta
    hs_key: str
    user_id: str
    refresh_token: str
    token: str

