import json
from typing import Dict, Any, List, Tuple

import redis
from redis.commands.search.field import TextField
from redis.commands.search.query import Query
from redis.commands.search.indexDefinition import IndexDefinition

from inrastructure.database.sql.models import User, UserPermissions


class RedisCache:

    def __init__(self):
        self.redis_server = redis.Redis(
            host='localhost',
            port=6379,
            db=0
        )
        self.redis_server.ft().create_index(
            (
                TextField("email"),
                TextField("configuration"),
            ),
            definition=IndexDefinition(
                prefix=["context:"]
            ),
        )

    def _user_data_dump(
            self,
            user: User
    ) -> Dict[str, Any]:
        result = {}
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
            f'context:{user_data["hash_identifier"]}',
            'email',
                user_data["hash_identifier"]["email"]
        )
        self.redis_server.hset(
            f'context:{user_data["hash_identifier"]}',
            'permission_conf',
                user_data["hash_identifier"]["permission_conf"]
        )