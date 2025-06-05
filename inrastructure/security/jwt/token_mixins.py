import logging
import os
from typing import Tuple

import jwt

from inrastructure.security.jwt.exceptions import DifferentTokenHashException, \
    TokenAudienceException, TokenDecoderException, TokenEncoderException
from inrastructure.security.jwt.helpers import create_hash

logger = logging.getLogger("root")

class TokenMethodBase:
    ALGORITHM = "HS256"

    @classmethod
    def generate_hash_for_search(cls):
        import uuid, datetime
        return (f"{uuid.uuid1()} - "
                f"{datetime.datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}")

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
            logger.exception(f"{cls.generate_hash_for_search()} -> "
                             f"Problem with encode user payload "
                             f"{payload} -> {e}")
            raise TokenEncoderException(
                status_code=403,
                detail=f"{cls.generate_hash_for_search()} -> "
                "Problem with token encode"
            )


class TokenDecoderMixin(TokenMethodBase):

    @classmethod
    def decode(cls, token: str) -> dict :
        try:
            return jwt.decode(
                token,
                key=os.getenv('hs_key'),
                algorithms=[cls.ALGORITHM])
        except jwt.DecodeError as e:
            logger.error(f"{cls.generate_hash_for_search()} "
                         f"Problem while decode token {e}")
            raise TokenDecoderException(
                status_code=403,
                detail=f"{cls.generate_hash_for_search()} -> "
                       f"Problem with token decode"
            )


class TokenValidatorMixin(TokenMethodBase):
    @classmethod
    def _custom_validate(cls, app, decoded_token_payload):
        tmp_decoded_token_payload = decoded_token_payload

        del tmp_decoded_token_payload["exp"]
        del tmp_decoded_token_payload["token_type"]

        at_hash = tmp_decoded_token_payload.pop("at_hash")
        if at_hash != create_hash(tmp_decoded_token_payload, cls.ALGORITHM):
            logger.error("Token stamp is incorrect")
            raise DifferentTokenHashException(
                status_code=403,
                detail=f"{cls.generate_hash_for_search()} -> "
                       f"Mismatch token hash"
            )

        if app not in decoded_token_payload["apps"]:
            logger.error("Requested application doesnt fit to token")
            raise TokenAudienceException(
                status_code=403,
                detail=f"{cls.generate_hash_for_search()} -> "
                f"User have not access to app"
            )

    @classmethod
    def validate(cls, token, app) -> Tuple[bool, dict]:
        if not (
            hasattr(cls, "decode")
            and callable(getattr(cls, "decode"))
        ):
            raise NotImplemented("Implement decode method")

        decoded: dict = cls.decode(token)
        cls._custom_validate(app, decoded)
        return True, decoded["payload"]
