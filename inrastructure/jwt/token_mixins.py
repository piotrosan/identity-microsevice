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
    decoded_token = None

    def custom_validate(self, app):
        tmp_decoded_token_payload = self.decoded_token.copy()

        del tmp_decoded_token_payload["exp"]

        at_hash = tmp_decoded_token_payload.pop("at_hash")
        if at_hash != create_hash(tmp_decoded_token_payload, self.ALGORITHM):
            logger.error("Token stamp is incorrect")
            raise DifferentTokenHash("Mismatch token hash")

        if app not in self.decoded_token["aud"]:
            logger.error("Requested application doesnt fit to token")
            raise TokenAudience("User have not access to app")

    def validate(self, token, app) -> bool:
        if not (
            hasattr(self, "decode")
            and callable(getattr(self, "decode"))
        ):
            raise NotImplemented("Implement decode method")

        self.decoded_token = self.decode(token)
        self.custom_validate(app)
        return True
