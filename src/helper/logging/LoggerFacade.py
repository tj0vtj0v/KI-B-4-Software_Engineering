import logging

from src.helper.logging.LogLevel import LogLevel
from src.helper.logging.LoggerInterface import LoggerInterface


class LoggerFacade(LoggerInterface):
    def __init__(self, level: LogLevel = LogLevel.INFO, service: str = "DefaultService"):
        self._logger = logging.getLogger()
        self._service = service

        if not self._logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '[%(asctime)s] [%(threadName)s] %(levelname)s: %(message)s', datefmt='%H:%M:%S'
            )
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)

        self._logger.setLevel(level)

    def log(self, message: str, level: LogLevel = LogLevel.INFO) -> None:
        if len(message) > 0:
            self._logger.log(level, f"{self._service} -> {message}")

    def set_level(self, level: LogLevel) -> None:
        self._logger.setLevel(level)
