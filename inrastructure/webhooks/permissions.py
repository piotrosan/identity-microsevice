import sys
from asyncio import Task
from types import FrameType
from typing import List, Dict

from inrastructure.cache.api.redis import RedisCache
from inrastructure.database.sql.models import User
from inrastructure.logger_sys.settings.logger_conf import logger
from inrastructure.requester_with_async.async_request import AsyncRequester


class UserPermissionFromMicroservicesApps:

    redis = None
    mcr_srv_cxt = None
    results = None

    def __init__(self, u: User):
        self.user = u
        self.redis = RedisCache()
        self.mcr_srv_cxt: List[dict] = self.redis.get_mcrsrv_for_usr_cxt(u)

    def _prepare_async_for_get_perm(self):
        data = [
            {
                'url': req['callback_url'],
                'method': req['method'],
                'headers': {
                    'Authorization': self.user.get_access_token([req['id']])
                },
            }  for req in self.mcr_srv_cxt
        ]
        return AsyncRequester(data)

    def _prepare_async_for_create_perm(self):
        data = [
            {
                'url': '/permission/user_group_role',
                'method': 'POST',
                'headers': {
                    'Authorization': self.user.get_access_token([req['id']])
                },
            }  for req in self.mcr_srv_cxt[0]
        ]
        return AsyncRequester(data)

    @classmethod
    def _transform_exception_to_log(
            self,
            r: BaseException
    ) -> str:
        tb = sys.exception().__traceback__
        return f'{r.with_traceback(tb)}'

    def get_permissions(self):
        a = self._prepare_async_for_get_perm()
        tasks: List[Task] = a.get_tasks()
        self.results = [{
            'result': task.result(),
            'exception': task.exception(),
            'stack': task.get_stack(),
            'fail': True if task.exception() else False
        }
            for task in tasks
        ]
        a.close_loop()

    def create_permissions(self):
        a = self._prepare_async_for_create_perm()
        tasks: List[Task] = a.get_tasks()
        self.results = [{
            'result': task.result(),
            'exception': task.exception(),
            'stack': task.get_stack(),
            'fail': True if task.exception() else False
        }
            for task in tasks
        ]
        a.close_loop()

    @classmethod
    def get_result(cls, u: User, kind: str) -> List[dict]:
        self = cls(u)
        {
            'create': self.create_permissions,
            'get': self.get_permissions
        }[kind]()
        [
            logger.exception(
                self._transform_exception_to_log(r['exception'])
            )
            for r in self.results if r['fail']
        ]
        return [r['result'] for r in self.results if not r['fail']]
