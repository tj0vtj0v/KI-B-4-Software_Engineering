from src.helper.Logger import Logger
from src.helper.logging.LogLevel import LogLevel


class Door:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.logger = Logger("DoorControl")
        self.opened = False

    def open(self):
        if not self.opened:
            self.opened = True
            self.logger.log("Door is now open.", LogLevel.INFO)
        else:
            self.logger.log("Door is already open.", LogLevel.WARNING)

    def close(self):
        if self.opened:
            self.opened = False
            self.logger.log("Door is now closed.", LogLevel.INFO)
        else:
            self.logger.log("Door is already closed.", LogLevel.WARNING)
