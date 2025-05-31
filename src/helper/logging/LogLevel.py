import logging
from enum import IntEnum


class LogLevel(IntEnum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            try:
                return cls[value.upper()]
            except KeyError:
                pass
        return super()._missing_(value)
