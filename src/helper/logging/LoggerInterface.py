from abc import ABC, abstractmethod

from src.helper.logging.LogLevel import LogLevel


class LoggerInterface(ABC):
    """
    Abstract base class for logger implementations.

    Defines the interface for logging messages at various log levels and for setting the current log level.
    """

    @abstractmethod
    def log(self, message: str, level: LogLevel = LogLevel.INFO) -> None:
        """
        Log a message with the specified log level.

        :param message: The message to log.
        :type message: str
        :param level: The log level for the message. Defaults to LogLevel.INFO.
        :type level: LogLevel
        :return: None
        """
        pass

    @abstractmethod
    def set_level(self, level: LogLevel) -> None:
        """
        Set the current log level for the logger.

        :param level: The log level to set.
        :type level: LogLevel
        :return: None
        """
        pass
