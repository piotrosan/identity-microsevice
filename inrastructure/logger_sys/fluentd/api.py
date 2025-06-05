from fluent import sender
from fluent import event

class FluentdAPI:

    host = 'fluentd'
    port = '24224'

    def __init__(self, tag: str):
        sender.setup(tag, host=self.host, port=self.port)

    def send(self, label: str, data: dict):
        event.Event(label, data)