import redis
import json
import logging
from typing import Dict, Any, List, Tuple, Awaitable

from inrastructure.cache.exception.cache import CacheHttpException
from inrastructure.database.sql.models import User, UserPermissions

logger = logging.getLogger('root')


class RedisCache:

    PREFIX = 'context:{user_identifier}'

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
        permission = user.user_permissions[0]
        result[user.hash_identifier]['permission_conf'] = permission.configuration
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
        self.redis_server.hset(
            name=self.PREFIX.format(user_identifier=user.hash_identifier),
            key='permission_conf',
            value=json.dumps(user_data[user.hash_identifier]["permission_conf"])
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

        permission_conf = self.redis_server.hget(
            self.PREFIX.format(user_identifier=user.hash_identifier),
            'permission_conf'
        )
        if permission_conf != '':
            logger.critical('There is no permission configuration')
            raise CacheHttpException(
                detail='There is no permission configuration',
                status_code=400
            )

        return {
            'context_address': self.PREFIX.format(
                user_identifier=user.hash_identifier),
            'email': email,
            'permission_conf': json.loads(permission_conf)
        }
