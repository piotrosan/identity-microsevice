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
            all_context: List[
                Tuple[
                    User,
                    UserPermissions,
                ]
            ]
    ) -> Dict[str, Any]:
        result = {}
        for auc in all_context:
            user = auc[0]
            permission = auc[1]
            result[user.hash_identifier]['permission_conf'] = permission.configuration
            result[user.hash_identifier]['email'] = user.email
        return result

    def set_context(
            self,
            all_context: List[
                Tuple[
                    User,
                    UserPermissions,
                ]
            ]
    ):
        user_data = self._user_data_dump(all_context)
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