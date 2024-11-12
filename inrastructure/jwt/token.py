import abc
import dataclasses
import os
from abc import abstractclassmethod, ABCMeta
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from uuid import UUID

from inrastructure.jwt.token_mixins import TokenCreator, TokenValidator


@dataclass
class AbstractToken(abc.ABC):
    exp: datetime
    iss: str
    at_hash: str
    token_type: str
    user_identifier: str

    @abc.abstractmethod
    def _encode(self, payload: dict) -> str:
        raise NotImplemented

    @abc.abstractmethod
    def _create_hash(self, payload: dict) -> str:
        raise NotImplemented

    @classmethod
    @abc.abstractmethod
    def decode(cls, token: str) -> dict :
        raise NotImplemented


@dataclass
class Token(TokenCreator, TokenValidator, AbstractToken):
    NOT_COPY_TO_HASH = ("exp", "token_type")

    def set_iss(self):
        self.iss = os.getenv('token_iss')

    def set_user_data(self, user_data: dict):
        self.__dict__.update(user_data)

    def _get_dump_payload(self):
        return dataclasses.asdict(self)

    def set_at_hash(self):
        dump_payload = self._get_dump_payload()
        for remove_attr in self.NOT_COPY_TO_HASH:
            del dump_payload[remove_attr]

        self.at_hash = self._create_hash(dump_payload)

    def get_user_identifier(self) -> UUID:
        try:
            return UUID(self.user_identifier)
        except Exception as e:
            raise ValueError("Not correct user identifier")


@dataclass
class AccessToken(Token):

    def set_exp(self):
        self.exp = datetime.now(
            tz=timezone.utc
        ) + timedelta(
            **{os.getenv('token_exp_time'): os.getenv('token_exp_delta')}
        )

    def get_access_token(self, user_data: dict) -> str:
        return self._encode(self._get_dump_payload())

@dataclass
class RefreshToken(Token):
    NOT_COPY_FROM_REFRESH = ("exp", "token_type")

    def set_exp(self):
        self.exp = datetime.now(
            tz=timezone.utc
        ) + timedelta(
            **{
                os.getenv('refresh_token_exp_time'):
                    os.getenv('refresh_token_exp_delta')
            }
        )

    def get_access_token(self) -> str:
        pass

    def get_refresh_token(self, token: str):
        pass

    @classmethod
    def from_token(cls, refresh_token: str):
        return RefreshToken(
            ** {
                k: v for k, v in cls.decode(refresh_token)
                if k not in cls.NOT_COPY_FROM_REFRESH
            })

