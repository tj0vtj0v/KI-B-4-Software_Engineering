from abc import ABC, abstractmethod

from src.helper.logging.LogLevel import LogLevel


class LoggerInterface(ABC):
    @abstractmethod
    def log(self, message: str, level: LogLevel = LogLevel.INFO) -> None:
        pass

    @abstractmethod
    def set_level(self, level: LogLevel) -> None:
        pass
