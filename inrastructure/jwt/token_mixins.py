import logging
import os
import json
from _datetime import datetime, timezone, timedelta
from uuid import UUID

import jwt
from dataclasses import dataclass

from inrastructure.jwt.exceptions import DifferentTokenHash, TokenAudience
from inrastructure.jwt.helpers import create_hash

logger = logging.getLogger("root")

class TokenMethodBase:
    ALGORITHM = "HS256"


class TokenEncoderMixin(TokenMethodBase):

    @classmethod
    def encode(cls, payload: dict) -> str:
        try:
            return jwt.encode(
                payload,
                os.getenv('hs_key'),
                algorithm=cls.ALGORITHM
            )
        except Exception as e:
            logger.exception(f"Problem with encode user payload {payload} -> {e}")
            raise ValueError("Problem with token encode")


class TokenDecoderMixin(TokenMethodBase):

    @classmethod
    def decode(cls, token: str) -> dict :
        try:
            return jwt.decode(
                token,
                key=os.getenv('hs_key'),
                algorithms=[cls.ALGORITHM])
        except jwt.DecodeError as e:
            logger.error(f"Problem while decode token {e}")
            raise ValueError("Problem with token decode")


class TokenValidatorMixin(TokenMethodBase):

    @classmethod
    def _custom_validate(cls, app, decoded_token_payload):
        tmp_decoded_token_payload = decoded_token_payload

        del tmp_decoded_token_payload["exp"]
        del tmp_decoded_token_payload["token_type"]

        at_hash = tmp_decoded_token_payload.pop("at_hash")
        if at_hash != create_hash(tmp_decoded_token_payload, cls.ALGORITHM):
            logger.error("Token stamp is incorrect")
            raise DifferentTokenHash("Mismatch token hash")

        if app not in decoded_token_payload["apps"]:
            logger.error("Requested application doesnt fit to token")
            raise TokenAudience("User have not access to app")

    @classmethod
    def validate(cls, token, app) -> bool:
        if not (
            hasattr(cls, "decode")
            and callable(getattr(cls, "decode"))
        ):
            raise NotImplemented("Implement decode method")

        cls._custom_validate(app, cls.decode(token))
        return True
