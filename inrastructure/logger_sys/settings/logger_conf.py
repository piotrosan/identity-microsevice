import logging.config
from inrastructure.logger_sys.handlers import FluentdHandler

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        # "db_formatter": {
        #     "format": "app=%(app)s %(funcName)s() L%(lineno)-4d %(message)s call_trace=%(pathname)s L%(lineno)-4d"
        # },
        "file_formatter": {
            "format": "DateTime=%(asctime)s loglevel=%(levelname)-6s  ;"
                      "func=%(funcName)s() ;"
                      "Line=%(lineno)-4d ;"
                      "message=%(message)s ;"
                      "call_trace=%(pathname)s;;"
        },
    },
    "handlers": {
        "std_handler": {
            "class": "logging.StreamHandler",
            "formatter": "file_formatter",
            'stream': 'ext://sys.stdout'
        },
        # "fluentd_handler": {
        #     "class": f"{FluentdHandler.__module__}.FluentdHandler",
        #     "formatter": "db_formatter",
        # },
    },
    "loggers" : {
        "root": {
            # "handlers": ["std_handler", "fluentd_handler"],
            "handlers": ["std_handler"],
            "level": "DEBUG",
            "propagate": True
            }
        }
})

logger = logging.getLogger('root')