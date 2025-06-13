import logging

from src.helper.logging.LogLevel import LogLevel
from src.helper.logging.LoggerInterface import LoggerInterface


class LoggerFacade(LoggerInterface):
    """
    Facade for Python's logging module, providing a unified logging interface.

    :param level: The initial logging level to set for the logger.
    :type level: LogLevel
    :param service: The name of the service or component using the logger.
    :type service: str
    """

    def __init__(self, level: LogLevel = LogLevel.INFO, service: str = "DefaultService") -> None:
        """
        Initialize the LoggerFacade with a specified log level and service name.

        :param level: The logging level to set for the logger. Defaults to LogLevel.INFO.
        :type level: LogLevel
        :param service: The name of the service or component using the logger. Defaults to "DefaultService".
        :type service: str
        :return: None
        """
        self._logger: logging.Logger = logging.getLogger()
        self._service: str = service

        if not self._logger.handlers:
            handler: logging.StreamHandler = logging.StreamHandler()
            formatter: logging.Formatter = logging.Formatter(
                '[%(asctime)s] [%(threadName)s] %(levelname)s: %(message)s', datefmt='%H:%M:%S'
            )
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)

        self._logger.setLevel(level)

    def log(self, message: str, level: LogLevel = LogLevel.INFO) -> None:
        """
        Log a message with the specified log level.

        :param message: The message to log.
        :type message: str
        :param level: The logging level to use. Defaults to LogLevel.INFO.
        :type level: LogLevel
        :return: None
        """
        if len(message) > 0:
            self._logger.log(level, f"{self._service} -> {message}")

    def set_level(self, level: LogLevel) -> None:
        """
        Set the logging level for the logger.

        :param level: The new logging level to set.
        :type level: LogLevel
        :return: None
        """
        self._logger.setLevel(level)
