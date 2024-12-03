import abc
import dataclasses
import os
from abc import ABC
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Literal
from uuid import UUID

from inrastructure.jwt.helpers import create_hash
from inrastructure.jwt.token_mixins import (
    TokenValidatorMixin,
    TokenEncoderMixin,
    TokenDecoderMixin
)

@dataclass
class AbstractToken(ABC):
    exp: datetime | None = None
    iss: str | None = None
    at_hash: str | None = None
    token_type: str | None = None
    user_identifier: str | None = None

    @classmethod
    @abc.abstractmethod
    def encode(cls, payload: dict) -> str:
        raise NotImplemented

    @classmethod
    @abc.abstractmethod
    def decode(cls, token: str) -> dict :
        raise NotImplemented

    @abc.abstractmethod
    def validate(self, token: str) -> bool:
        raise NotImplemented

    # @classmethod
    # @abc.abstractmethod
    # def from_str(cls, token: str) -> "AbstractToken":
    #     raise NotImplemented


class Token(
    TokenEncoderMixin,
    TokenDecoderMixin,
    TokenValidatorMixin,
    AbstractToken
):
    NOT_COPY_TO_HASH = ("exp", "token_type")

    def set_iss(self, iss):
        self.iss = iss

    def set_user_data(self, user_data: dict):
        self.__dict__.update(user_data)

    def _get_dump_payload(self):
        return dataclasses.asdict(self)

    def _set_at_hash(self):
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

    def set_exp(self):
        self.exp = datetime.now(
            tz=timezone.utc
        ) + timedelta(
            **{os.getenv('token_exp_time'): float(os.getenv('token_exp_delta'))}
        )
    @property
    def access_token(self) -> str:
        return self.encode(self._get_dump_payload())


    def prepare_access_token(self, app: str, user_data: dict):
        self.set_iss(app)
        self.set_user_data(user_data)
        self.set_exp()
        self._set_at_hash()


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

    def get_access_token_obj(self, refresh_token: str) -> AccessToken:
        return AccessToken(**{
            k: v for k, v in self.decode(refresh_token)
            if k not in self.NOT_COPY_FROM_REFRESH
        })

    def get_refresh_token(self) -> str:
        self._set_iss()
        self.set_exp()
        self._set_at_hash()
        return self.encode(self._get_dump_payload())
