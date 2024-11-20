from enum import Enum
import datetime
from typing import Any, List, Dict


class Target(Enum):
    FILE = 'file'
    CONSOLE = 'console'
    DATABASE = 'database'

class LogMessage:

    content_message = None

    def prepare_message_content(self, data, level) -> dict:
        self.content_message = {
            "timestamp": datetime.datetime.now(),
            "level": level if level else 'CRITICAL',
            "data": data.get("message"),
            "app_class": data.get("app_class")
        }

    def message_for_file(self) -> str:
        return f"{self.content_message['timestamp']} --> " \
                f"{self.content_message['level']} --> " \
               f"{self.content_message['app_class']} --> " \
               f"{self.content_message['data']}"

    def message_for_database(self) -> dict:
        return self.content_message

class Logger:

    target = Target

    def __init__(self, database, file):
        self.database = database
        self.file = file

    def _log_to_file(self, data, level) -> None:
        log_message = LogMessage()
        log_message.prepare_message_content(data, level)
        self.file.write(log_message.message_for_file())

    def _log_to_database(self, data, level) -> None:
        log_message = LogMessage()
        log_message.prepare_message_content(data, level)
        self.database.save(log_message.message_for_database())

    def log(self, targets: List[Target], data: Dict, level) -> None:
        log_target = {
            'file': self._log_to_file(data, level),
            'database': self._log_to_database(data, level)
        }
        [log_target[target](data, level) for target in targets]



