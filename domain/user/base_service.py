import logging

from domain.http_exception_user import UserServiceGenericException

logger = logging.getLogger("root")


class Service:
    model = None

    def __init__(self):
        if not self.model:
            logger.error(f"Service class dont have fill model parameter")
            raise UserServiceGenericException()
