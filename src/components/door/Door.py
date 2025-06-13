from src.helper.Logger import Logger
from src.helper.logging.LogLevel import LogLevel


class Door:
    """
    Singleton class representing a door with open and close functionality.

    This class ensures only one instance exists and provides methods to open and close the door,
    logging each action.
    """

    _instance: 'Door' = None

    def __new__(cls) -> 'Door':
        """
        Create or return the singleton instance of Door.

        :return: The singleton instance of Door.
        :rtype: Door
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """
        Initialize the Door instance.

        Sets up the logger and initializes the door state as closed.
        """
        self.logger: Logger = Logger("DoorControl")
        self.opened: bool = False

    def open(self) -> None:
        """
        Open the door if it is not already open.

        Logs the action at INFO level if the door is opened, or at WARNING if already open.

        :return: None
        """
        if not self.opened:
            self.opened = True
            self.logger.log("Door is now open.", LogLevel.INFO)
        else:
            self.logger.log("Door is already open.", LogLevel.WARNING)

    def close(self) -> None:
        """
        Close the door if it is not already closed.

        Logs the action at INFO level if the door is closed, or at WARNING if already closed.

        :return: None
        """
        if self.opened:
            self.opened = False
            self.logger.log("Door is now closed.", LogLevel.INFO)
        else:
            self.logger.log("Door is already closed.", LogLevel.WARNING)
