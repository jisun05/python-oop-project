import logging
import logging.config           
from contextvars import ContextVar  


request_id_context: ContextVar[str] = ContextVar("request_id", default="-")


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_context.get("-")
        return True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "filters": {"rid": {"()": RequestIdFilter}},

    "formatters": {
        "default": {
            "format": "%(asctime)s %(levelname)s [%(name)s] [rid=%(request_id)s] %(message)s"
        }
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "filters": ["rid"],
            "formatter": "default",
            "stream": "ext://sys.stdout",
        }
    },

    "loggers": {
        "app": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"level": "INFO"},

        "sqlalchemy.engine": {"level": "WARNING"},
    },

    "root": {"handlers": ["console"], "level": "INFO"},
}


def setup_logging():
    logging.config.dictConfig(LOGGING)
