from datetime import datetime
from beanie import Document
from pydantic import Field

class Log(Document):
    timestamp: datetime = Field(default_factory=datetime.now)
    level: str
    message: str
    app_class: str
