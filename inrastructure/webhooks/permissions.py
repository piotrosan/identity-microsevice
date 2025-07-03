import sys
from asyncio import Task
from types import FrameType
from typing import List

from inrastructure.cache.api.redis import RedisCache
from inrastructure.database.sql.models import User
from inrastructure.logger_sys.settings.logger_conf import logger
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
                'url': req['callback_url'],
                'method': req['method'],
                'headers': {
                    'Authorization': self.user.get_access_token([req['app']])
                },
            }  for req in self.registry[0]
        ]
        return AsyncRequester(data)

    @classmethod
    def _transform_exception_to_log(
            self,
            r: BaseException
    ) -> str:
        tb = sys.exception().__traceback__
        return f'{r.with_traceback(tb)}'



    @classmethod
    def get_permissions(cls, u: User) -> List[dict]:
        self = cls(u)
        req = self._prepare_req()
        tasks: List[Task] = req.get_data_from_requests()
        result = [{
            'result': task.result(),
            'exception': task.exception(),
            'stack': task.get_stack(),
            'fail': True if task.exception() else False
        }
            for task in tasks
        ]
        req.close_loop()

        [
            logger.exception(
                cls._transform_exception_to_log(r['exception'])
            )
            for r in result if r['fail']
        ]
        return [r for r in result if not r['fail']]