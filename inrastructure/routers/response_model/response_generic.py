from pydantic import BaseModel


import datetime

from pydantic import BaseModel, field_validator
from pydantic_core.core_schema import FieldValidationInfo


class GenericResponse(BaseModel):
    model_config = {"validate_default": True}

    timestamp: str
    message: str

    @field_validator("timestamp", mode="before")
    def default_from_url(
            cls,
            timestamp: object,
            info: FieldValidationInfo
    ) -> str:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
