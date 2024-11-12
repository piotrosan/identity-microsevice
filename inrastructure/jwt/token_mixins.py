import os
import json
from _datetime import datetime, timezone, timedelta
from uuid import UUID

import jwt
from dataclasses import dataclass

from inrastructure.jwt.exceptions import DifferentTokenHash, TokenAudience

class TokenMethodBase:
    ALGORITHM = "HS256"


class TokenHelper(TokenMethodBase):

    def _create_hash(self, payload: dict) -> str:
        alg_obj = jwt.get_algorithm_by_name(self.ALGORITHM)
        return alg_obj.compute_hash_digest(
            json.dumps(payload).encode('UTF-8')
        )


@dataclass
class TokenEncoder(TokenMethodBase):

    def _encode(self, payload: dict) -> str:
        try:
            return jwt.encode(
                payload,
                os.getenv('hs_key'),
                algorithm=self.ALGORITHM
            )
        except Exception as e:
            # todo add log exception to log file
            raise ValueError("Problem with token encode")


class TokenDecoder(TokenMethodBase):

    @classmethod
    def decode(cls, token: str) -> dict :
        try:
            return jwt.decode(
                token,
                key=os.getenv('hs_key'),
                algorithms=[cls.ALGORITHM])
        except jwt.DecodeError as e:
            # todo add log exception to log file
            raise ValueError("Problem with token decode")


@dataclass
class TokenValidator(TokenMethodBase):
    decoded_token = None

    def custom_validate(self, app):
        tmp_decoded_token_payload = self.decoded_token.copy()

        del tmp_decoded_token_payload["exp"]

        at_hash = tmp_decoded_token_payload.pop("at_hash")
        if at_hash != self._create_hash(tmp_decoded_token_payload):
            # todo add log exception to log file
            raise DifferentTokenHash("Mismatch token hash")

        if app not in self.decoded_token["aud"]:
            # todo add log exception to log file
            raise TokenAudience("User have not access to app")

    def validate(self, token, app) -> bool:
        self.decoded_token = self.decode(token)
        self.custom_validate(app)
        return True
