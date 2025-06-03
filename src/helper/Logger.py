from src.helper.config import DEFAULT_LOG_LEVEL
from src.helper.logging.LogLevel import LogLevel
from src.helper.logging.LoggerFacade import LoggerFacade
from src.helper.logging.LoggerInterface import LoggerInterface


class Logger(LoggerInterface):
    _instances: dict[str, LoggerFacade] = {}

    def __new__(cls, service: str, level: LogLevel = DEFAULT_LOG_LEVEL):
        if service not in cls._instances:
            cls._instances[service] = LoggerFacade(level, service)
        return cls._instances[service]
