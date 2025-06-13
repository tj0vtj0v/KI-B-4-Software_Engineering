from src.components.door.Door import Door
from src.helper.Logger import Logger
from src.helper.exceptions import DoorException
from src.helper.logging.LogLevel import LogLevel


class DoorController:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DoorController, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.logger = Logger("DoorControl")

        self.locked = False
        self.door = Door()

    def lock(self):
        if not self.door.opened:
            if self.locked:
                self.logger.log("Door is already locked.", LogLevel.INFO)
            else:
                self.logger.log("Door is now locked.", LogLevel.INFO)
                self.locked = True
        else:
            self.logger.log("Cannot lock the door while it is open.", LogLevel.WARNING)

    def unlock(self):
        if not self.locked:
            self.logger.log("Door is already unlocked.", LogLevel.INFO)
        else:
            self.logger.log("Door is now unlocked.", LogLevel.INFO)
            self.locked = False

    def check(self):
        self.logger.log(f"Door locked: {self.locked} and opened: {self.door.opened}", LogLevel.DEBUG)

        if self.locked and self.door.opened:
            self.logger.log("Door is locked and was forcefully opened.", LogLevel.CRITICAL)
            raise DoorException("Door is locked and was forcefully opened.")
