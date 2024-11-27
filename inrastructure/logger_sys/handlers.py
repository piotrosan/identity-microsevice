import logging
import traceback
from datetime import datetime

from inrastructure.database.nosql.database_api import MongoDbAPI
from inrastructure.logger_sys.fluentd.fluentd_api import FluentdAPI


class MongoDbHandler(logging.Handler):

    def __init__(self)-> None:
        database = "logdatabase"
        collection = "log"
        self.sender = MongoDbAPI(database_name=database)
        self.sender.raw_pymongo_api.get_database()
        self.sender.raw_pymongo_api.get_collection(collection)
        logging.Handler.__init__(self=self)

    def emit(self, record) -> None:
        self.sender.save({
            "message": record.message,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "level": record.levelname,
            "traceback": traceback.format_exc(),
            "action": record.funcName
        })


class FluentdHandler(logging.Handler):

    def __init__(self) -> None:
        self.sender = FluentdAPI("identity.service")
        logging.Handler.__init__(self=self)

    def emit(self, record) -> None:
        self.sender.send(record.funcName, {
            "message": record.message,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "level": record.levelname,
            "traceback": traceback.format_exc(),
        })