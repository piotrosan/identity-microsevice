import datetime
from typing import Any, List, Dict
import logging
from logging.config import dictConfig

dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "db_formatter": {
            "format": "%(funcName)s() L%(lineno)-4d %(message)s call_trace=%(pathname)s L%(lineno)-4d"
        },
        "file_formatter": {
            "format": "DateTime=%(asctime)s loglevel=%(levelname)-6s  %(funcName)s() L%(lineno)-4d %(message)s call_trace=%(pathname)s L%(lineno)-4d"
        },
    },
    "handlers": {
        "std_handler": {
            "class": "logging.StreamHandler",
            "formatter": "file_formatter",
            'stream': 'ext://sys.stdout'
        },
        # "mongo_handler": {
        #     "class": "infrastructure.logger_sys.handlers.MongoDbHandler",
        #     "formatter": "db_formatter",
        # },
        "fluentd_handler": {
            "class": "infrastructure.logger_sys.handlers.FluentdHandler",
            "formatter": "db_formatter",
        },
    },
    "loggers" : {
        "root": {
            "handlers": ["std_handler", "fluentd_handler"],
            "level": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            "propagate": True
            }
        }
})

