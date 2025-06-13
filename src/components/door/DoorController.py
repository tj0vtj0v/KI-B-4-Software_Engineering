from src.components.door.Door import Door
from src.helper.Logger import Logger
from src.helper.exceptions import DoorException
from src.helper.logging.LogLevel import LogLevel


class DoorController:
    """
    Singleton controller class for managing door operations such as locking, unlocking, and status checking.
    """

    _instance: 'DoorController' = None

    def __new__(cls, *args, **kwargs) -> 'DoorController':
        """
        Ensures only one instance of DoorController exists (Singleton pattern).

        :param args: Positional arguments.
        :param kwargs: Keyword arguments.
        :return: The singleton instance of DoorController.
        :rtype: DoorController
        """
        if cls._instance is None:
            cls._instance = super(DoorController, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """
        Initializes the DoorController with a logger, lock state, and a Door instance.
        """
        self.logger: Logger = Logger("DoorControl")
        self.locked: bool = False
        self.door: Door = Door()

    def lock(self) -> None:
        """
        Locks the door if it is closed and not already locked.
        Logs the action or warning if the door is open.

        :return: None
        """
        if not self.door.opened:
            if self.locked:
                self.logger.log("Door is already locked.", LogLevel.INFO)
            else:
                self.logger.log("Door is now locked.", LogLevel.INFO)
                self.locked = True
        else:
            self.logger.log("Cannot lock the door while it is open.", LogLevel.WARNING)

    def unlock(self) -> None:
        """
        Unlocks the door if it is currently locked.
        Logs the action or info if the door is already unlocked.

        :return: None
        """
        if not self.locked:
            self.logger.log("Door is already unlocked.", LogLevel.INFO)
        else:
            self.logger.log("Door is now unlocked.", LogLevel.INFO)
            self.locked = False

    def check(self) -> None:
        """
        Checks the current state of the door and logs the status.
        Raises a DoorException if the door is locked but found open.

        :raises DoorException: If the door is locked and open.
        :return: None
        """
        self.logger.log(f"Door locked: {self.locked} and opened: {self.door.opened}", LogLevel.DEBUG)

        if self.locked and self.door.opened:
            self.logger.log("Door is locked and was forcefully opened.", LogLevel.CRITICAL)
            raise DoorException("Door is locked and was forcefully opened.")
