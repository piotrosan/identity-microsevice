from enum import Enum
from typing import Any, List


class Target(Enum):
    FILE = 'file'
    CONSOLE = 'console'
    DATABASE = 'database'


class Logger:

    target = Target

    def log(self, target: List[Target], data: Any) -> None:
        pass
