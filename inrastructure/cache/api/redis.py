import redis
import json
import logging
from typing import Dict, Any, List, Tuple, Awaitable

from inrastructure.cache.exception.cache import CacheHttpException
from inrastructure.database.sql.models import User

logger = logging.getLogger('root')


class RedisCache:

    PREFIX = 'context:{user_identifier}'
    APP_PREFIX = 'apps_identifiers:'

    def __init__(self):
        self.redis_server = redis.Redis(
            host='localhost',
            port=6379,
            db=0
        )

    def _user_data_dump(
            self,
            user: User
    ) -> Dict[str, Any]:
        result = {user.hash_identifier: {}}
        result[user.hash_identifier]['email'] = user.email
        return result

    def set_context(
            self,
            user: User
    ):
        user_data = self._user_data_dump(user)
        self.redis_server.hset(
            name=self.PREFIX.format(user_identifier=user.hash_identifier),
            key='email',
            value=user_data[user.hash_identifier]["email"]
        )
        return self.PREFIX.format(user_identifier=user.hash_identifier)

    def get_context(self, user: User) -> dict[str, str | dict]:
        email = self.redis_server.hget(
            self.PREFIX.format(user_identifier=user.hash_identifier),
            'email'
        )
        if email != user.email:
            logger.critical('Email doesnt fit to user')
            raise CacheHttpException(
                detail='Email doesnt fit to user',
                status_code=400
            )

        return {
            'context_address': self.PREFIX.format(
                user_identifier=user.hash_identifier),
            'email': email,
        }

    def set_app_registry(self, app, name, na_me):
        result = self.redis_server.json().get(self.APP_PREFIX, '$')

        if not result:
            self.redis_server.json().set(
                name=self.APP_PREFIX,
                path='$',
                obj=[{'app': app, 'name': name, 'na_me': na_me}]
            )
            return

        exist = [
            True for index, res in enumerate(result[0])
            if res['app'] == app
        ]

        if not any(exist):
            self.redis_server.json().arrappend(
                self.APP_PREFIX,
                '$',
                {'app': app, 'name': name, 'na_me': na_me}
            )

    def unset_app_registry(self, app):
        result = self.redis_server.json().get(self.APP_PREFIX, '$')
        for index, res in enumerate(result[0]):
            if res['app'] == app:
                self.redis_server.json().delete(
                    self.APP_PREFIX,
                    f'$.[{index}]',
                )

    def get_app_registry(self) -> List[List[dict]]:
        return self.redis_server.json().get(self.APP_PREFIX, '$')
