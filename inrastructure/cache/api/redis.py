import json
from typing import Dict, Any, List, Tuple

import redis
from redis.commands.search.field import TextField
from redis.commands.search.query import Query
from redis.commands.search.indexDefinition import IndexDefinition

from inrastructure.database.sql.models import User, UserPermissions


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