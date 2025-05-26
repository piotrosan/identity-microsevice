import abc
import dataclasses
import os
from abc import ABC
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Literal, List
from uuid import UUID

from inrastructure.security.jwt.helpers import create_hash
from inrastructure.security.jwt.token_mixins import (
    TokenValidatorMixin,
    TokenEncoderMixin,
    TokenDecoderMixin
)


"""
“exp” (Expiration Time) Claim
“nbf” (Not Before Time) Claim
“iss” (Issuer) Claim
“aud” (Audience) Claim
“iat” (Issued At) Claim
"""


@dataclass
class AbstractToken(ABC):
    exp: datetime | None = None
    iss: str | None = None
    at_hash: str | None = None
    token_type: str | None = None
    user_identifier: str | None = None
    apps: List[str] | None = None

    @classmethod
    @abc.abstractmethod
    def encode(cls, payload: dict) -> str:
        raise NotImplemented

    @classmethod
    @abc.abstractmethod
    def decode(cls, token: str) -> dict :
        raise NotImplemented

    @classmethod
    @abc.abstractmethod
    def validate(cls, token: str) -> bool:
        raise NotImplemented


class Token(
    TokenEncoderMixin,
    TokenDecoderMixin,
    TokenValidatorMixin,
    AbstractToken
):
    NOT_COPY_TO_HASH = ("exp", "token_type", "at_hash")

    def set_iss(self):
        self.iss = os.getenv("iss")

    def set_user_data(self, user_data: dict):
        self.__dict__.update(user_data)

    def _get_dump_payload(self):
        return dataclasses.asdict(self)

    def set_at_hash(self):

        dump_payload = self._get_dump_payload()
        for remove_attr in self.NOT_COPY_TO_HASH:
            del dump_payload[remove_attr]
        self.at_hash = create_hash(dump_payload, self.ALGORITHM)

    def get_user_identifier(self) -> UUID:
        try:
            return UUID(self.user_identifier)
        except Exception as e:
            raise ValueError("Not correct user identifier")


class AccessToken(Token):
    token_type = Literal["access_token"]

    def set_exp(self):
        self.exp = datetime.now(
            tz=timezone.utc
        ) + timedelta(
            **{os.getenv('token_exp_time'): float(os.getenv('token_exp_delta'))}
        )

    @property
    def access_token(self) -> str:
        return self.encode(self._get_dump_payload())


class RefreshToken(Token):
    token_type: Literal["refresh_token"]

    NOT_COPY_FROM_REFRESH = ("exp", "token_type")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_exp(self):
        self.exp = datetime.now(
            tz=timezone.utc
        ) + timedelta(
            **{
                os.getenv('refresh_token_exp_time'):
                    os.getenv('refresh_token_exp_delta')
            }
        )

    @property
    def refresh_token(self) -> str:
        return self.encode(self._get_dump_payload())

    @classmethod
    def access_token(cls, refresh_token: str) -> AccessToken:
        access = AccessToken(**{
            k: v for k, v in cls.decode(refresh_token)
            if k not in cls.NOT_COPY_FROM_REFRESH
        })
        return access

    @classmethod
    def recreate(cls, refresh_token: str) -> "RefreshToken":
        refresh = cls(**{
            k: v for k, v in cls.decode(refresh_token)
        })
        return refresh

class TokenFactory:

    @classmethod
    def create_access_token(cls, data: dict) -> AccessToken:
        access = AccessToken()
        access.set_user_data(data["user_data"])
        access.set_exp()
        access.set_iss()
        access.set_at_hash()
        return access

    @classmethod
    def create_refresh_token(cls, data: dict) -> RefreshToken:
        refresh = RefreshToken()
        refresh.set_user_data(data["user_data"])
        refresh.set_exp()
        refresh.set_iss()
        refresh.set_at_hash()
        return refresh

    @classmethod
    def recreate_refresh_token(cls, refresh_token_old: str) -> RefreshToken:
        refresh_token = RefreshToken.recreate(refresh_token_old)
        refresh_token.set_exp()
        return refresh_token


    @classmethod
    def access_token_from_refresh_token(cls, token: str) -> AccessToken:
        access_token = RefreshToken.access_token(token)
        access_token.set_exp()
        return access_token
