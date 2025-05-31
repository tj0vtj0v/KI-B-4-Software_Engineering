from src.helper.logging.LogLevel import LogLevel
from src.helper.logging.LoggerFacade import LoggerFacade
from src.helper.logging.LoggerInterface import LoggerInterface


class Logger(LoggerInterface):
    _instances: dict[str, LoggerFacade] = {}

    def __new__(cls, service: str, level: LogLevel = LogLevel.INFO):
        if service not in cls._instances:
            cls._instances[service] = LoggerFacade(level, service)
        return cls._instances[service]


def log(self, message: str, level: LogLevel = LogLevel.INFO) -> None:
    self._instance.log(message, level)


def set_level(self, level: LogLevel) -> None:
    self._instance.set_level(level)
