"""
Logger module providing a singleton logger per service.

This module defines the Logger class, which ensures that only one logger instance
exists per service name. It uses the LoggerFacade to handle logging operations.
"""

from src.helper.config import DEFAULT_LOG_LEVEL
from src.helper.logging.LogLevel import LogLevel
from src.helper.logging.LoggerFacade import LoggerFacade
from src.helper.logging.LoggerInterface import LoggerInterface


class Logger(LoggerInterface):
    """
    Singleton Logger class that provides a logger instance per service.

    This class ensures that only one LoggerFacade instance exists for each service name.
    """

    _instances: dict[str, LoggerFacade] = {}

    def __new__(cls, service: str, level: LogLevel = DEFAULT_LOG_LEVEL) -> LoggerFacade:
        """
        Create or retrieve a singleton LoggerFacade instance for the given service.

        :param service: The name of the service for which the logger is created.
        :type service: str
        :param level: The log level to use for the logger. Defaults to DEFAULT_LOG_LEVEL.
        :type level: LogLevel
        :return: A singleton LoggerFacade instance for the specified service.
        :rtype: LoggerFacade
        """
        if service not in cls._instances:
            cls._instances[service] = LoggerFacade(level, service)
        return cls._instances[service]
