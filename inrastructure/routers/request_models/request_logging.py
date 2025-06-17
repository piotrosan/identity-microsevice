from typing import List
from pydantic import BaseModel


class LoggingData(BaseModel):
    app: str
    level: int
    message: str

