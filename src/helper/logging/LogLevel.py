import logging
from enum import IntEnum
from typing import Any, Optional


class LogLevel(IntEnum):
    """
    Enumeration for log levels, mapping to Python's standard logging levels.
    """

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    @classmethod
    def _missing_(cls, value: Any) -> Optional["LogLevel"]:
        """
        Handle missing values by attempting to match string names to enum members.

        :param value: The value to resolve, can be a string or an integer.
        :type value: Any
        :return: The corresponding LogLevel member if found, otherwise None.
        :rtype: Optional[LogLevel]
        """
        if isinstance(value, str):
            try:
                return cls[value.upper()]
            except KeyError:
                pass
        return super()._missing_(value)
