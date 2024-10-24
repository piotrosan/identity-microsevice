import os
import jwt
from dataclasses import dataclass


@dataclass
class JwtCreator:
    email: str

    def _encode(self, payload: dict) -> str:
        key = os.getenv('hs_key')
        return jwt.encode(payload, key, algorithm="HS256")


    def _create_payload(self, users_data: dict):

        payload ={
            ""
        }

    def get_jwt(self):
        pass