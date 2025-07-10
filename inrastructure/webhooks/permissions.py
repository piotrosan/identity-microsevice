import sys
from asyncio import Task
from enum import Enum
from typing import List, Dict

from inrastructure.cache.api.redis import RedisCache
from inrastructure.database.sql.models import User
from inrastructure.logger_sys.settings.logger_conf import logger
from inrastructure.requester_with_async.async_request import AsyncRequester


class PermissionOperation(Enum):
    GET = 'get'
    CREATE = 'create'


class BasePermissionOperation:
    _apps_ids = None
    _user = None
    _redis = None
    _mcr_srv_cxt = None
    _results = None

    def __init__(self, u: User, app_ids: List[dict]=None):
        self._user = u
        self._redis = RedisCache()
        self._apps_ids = app_ids

    def _prepare_async(self):
        raise NotImplemented

    def run(self):
        a = self._prepare_async()
        tasks: List[Task] = a.get_tasks()
        self._results = [{
            'result': task.result(),
            'exception': task.exception(),
            'stack': task.get_stack(),
            'fail': True if task.exception() else False
        }
            for task in tasks
        ]
        a.close_loop()


class CreatePermissionsInMicroservice(BasePermissionOperation):

    def __init__(self, apps_ids: List[str], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apps_ids = apps_ids
        self._mcr_srv_cxt: List[dict] = self._redis.get_mcrsrv_for_app_cxt(
            apps_ids
        )

    def _prepare_async(self):
        data = [
            {
                'url': req['callback_url'],
                'method': req['method'],
                'headers': {
                    'Authorization': self._user.get_access_token([req['id']])
                },
            }  for req in self._mcr_srv_cxt
        ]
        return AsyncRequester(data)


class GetPermissionFromMicroservice(BasePermissionOperation):

    def __init__(self, u: User, *args, **kwargs):
        super().__init__(u, *args, **kwargs)
        self._mcr_srv_cxt: List[dict] = self._redis.get_mcrsrv_for_usr_cxt(u)

    def _prepare_async(self):
        data = [
            {
                'url': req['callback_url'],
                'method': req['method'],
                'headers': {
                    'Authorization': self._user.get_access_token([req['id']])
                },
            }  for req in self._mcr_srv_cxt
        ]
        return AsyncRequester(data)


class UserPermission:

    @classmethod
    def _transform_exception_to_log(
            cls,
            r: BaseException
    ) -> str:
        tb = sys.exception().__traceback__
        return f'{r.with_traceback(tb)}'

    @classmethod
    def get_result_operation(
            cls,
            u: User,
            kind: PermissionOperation,
            apps_ids: List[str]=None
    ) -> List[dict]:
        self = {
            PermissionOperation.CREATE: CreatePermissionsInMicroservice,
            PermissionOperation.GET: GetPermissionFromMicroservice
        }[kind](u, apps_ids)
        self.run()
        [
            logger.exception(
                cls._transform_exception_to_log(r['exception'])
            )
            for r in self._results if r['fail']
        ]
        return [r['result'] for r in self._results if not r['fail']]
