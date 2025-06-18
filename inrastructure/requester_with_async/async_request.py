from typing import List, Dict
import asyncio

from inrastructure.requester_with_async.requester import Requester


class AsyncRequester(Requester):

    requesters = None
    loop = None
    tasks = None

    def __init__(self, request_datas_with_params: List[Dict[str, str | dict]]):
        self.loop = asyncio.get_event_loop()
        self.tasks = [
            self._prepare_tasks(**val)
            for val in request_datas_with_params
        ]
        self.build_session()

    def _prepare_tasks(self, **kwargs):
        self.build_request(**kwargs)
        return self.loop.create_task(self.send())

    async def get_data_from_requests(self):
        self.loop.run_until_complete(asyncio.gather(*self.requesters))
        return self.tasks
