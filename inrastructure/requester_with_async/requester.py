import requests


class Requester:
    r = None
    session = None

    def _build_request(self, **kwargs):
        req = requests.Request(
            method=kwargs['method'],
            headers=kwargs.get('headers', None),
            url=kwargs["url"],
            params=kwargs.get('params', None),
            json=kwargs.get('json', None),
        )
        self.r = req.prepare()

    def _build_session(self):
        self.session = requests.Session()

    async def send(self):
        return self.session.send(self.r)