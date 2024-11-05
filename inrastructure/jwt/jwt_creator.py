import os
import json
from _datetime import datetime, timezone, timedelta
from pickletools import pydict

import jwt
from dataclasses import dataclass

from inrastructure.jwt.exceptions import DifferentTokenHash, TokenAudience


@dataclass
class JwtCreator:
    ALGORITHM = "HS256"

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


    def _create_hash(self, payload: dict):
        alg_obj = jwt.get_algorithm_by_name(self.ALGORITHM)
        return alg_obj.compute_hash_digest(
            json.dumps(payload).encode('UTF-8')
        )

    def _create_payload(self, users_data: dict):
        payload ={"iss": os.getenv('token_iss')}
        payload.update(users_data)
        payload.update({
            "at_hash": self._create_hash(payload)
        })
        payload.update({
            "exp": datetime.now(tz=timezone.utc) + timedelta(**{
                os.getenv('token_exp_time'): os.getenv('token_exp_delta')
            })
        })
        return payload

    def get_jwt(self, user_data):
        return self._encode(
            self._create_payload(user_data)
        )

    def _decode_jwt(self, token) -> dict :
        try:
            return jwt.decode(
                token,
                key=os.getenv('hs_key'),
                algorithms=[self.ALGORITHM])
        except jwt.DecodeError as e:
            # todo add log exception to log file
            raise ValueError("Problem with token decode")

    def validate(self, token, app):
        # verify under decode
        decoded_token = self._decode_jwt(token)

        # custom verify
        tmp_decoded_token_payload = decoded_token.copy()
        del tmp_decoded_token_payload["exp"]
        at_hash = tmp_decoded_token_payload.pop("at_hash")
        if at_hash != self._create_hash(tmp_decoded_token_payload):
            # todo add log exception to log file
            raise DifferentTokenHash("Mismatch token hash")

        if app not in decoded_token["aud"]:
            # todo add log exception to log file
            raise TokenAudience("User have not access to app")
