from typing import List

from inrastructure.cache.api.redis import RedisCache
from inrastructure.database.sql.models import User
from inrastructure.requester_with_async.async_request import AsyncRequester


class UserPermissionFromMicroservicesApps:

    redis = None
    registry = None

    def __init__(self, u: User):
        self.user = u
        self.redis = RedisCache()
        self.registry: List[List[dict]] = self.redis.get_app_registry()

    def _prepare_req(self):
        data = [
            {
                'url': v['url'],
                'method': v['method'],
                'headers': {'Authorization': self.user.get_access_token()},
            }  for k, v in self.registry[0][0].items()
        ]
        return AsyncRequester(data)

    async def get_permissions(self):
        req = self._prepare_req()
        return await req.get_data_from_requests()