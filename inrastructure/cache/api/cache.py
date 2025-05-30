import json
from typing import Dict, Any, List, Tuple

import redis
from redis.commands.search.field import TextField
from redis.commands.search.query import Query
from redis.commands.search.indexDefinition import IndexDefinition

from inrastructure.database.sql.models import User, ExternalLogin, UserGroup, \
    Role


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
                TextField("group_and_roles"),
            ),
            definition=IndexDefinition(
                prefix=["context:"]
            ),
        )

    def _user_data_dump(
            self,
            all_user_context: List[
                Tuple[
                    User,
                    ExternalLogin,
                    List[(UserGroup, List[Role])]
                ]
            ]
    ) -> Dict[str, Any]:
        result = {}
        for auc in all_user_context:
            user = auc[0]
            ugs = auc[2]
            result[user.hash_identifier]['groups_and_roles'] = {}
            for ug in ugs:
                result[user.hash_identifier]['groups_and_roles'][ug[0]] = ug[1]
            result[user.hash_identifier]['email']= user.email
        return result

    def set_context(
            self,
            all_user_context: List[
                Tuple[
                    User,
                    ExternalLogin,
                    List[(UserGroup, List[Role])]
                ]
            ]
    ):
        user_data = self._user_data_dump(all_user_context)
        self.redis_server.hset(
            f'context:{user_data["hash_identifier"]}',
            'email',
                user_data["hash_identifier"]["email"]
        )

        self.redis_server.hset(
            f'context:{user_data["hash_identifier"]}',
            'group_and_roles',
                json.dumps(user_data["hash_identifier"]["group_and_roles"])
        )
