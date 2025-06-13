from src.components.alarm.Alarm import Alarm
from src.helper.Logger import Logger
from src.helper.logging.LogLevel import LogLevel


class AlarmController:
    """
    Singleton controller class for managing the alarm system.

    This class provides methods to activate, deactivate, and check the status of the alarm.
    """

    _instance: 'AlarmController' = None

    def __new__(cls) -> 'AlarmController':
        """
        Create or return the singleton instance of AlarmController.

        :return: The singleton instance of AlarmController.
        :rtype: AlarmController
        """
        if cls._instance is None:
            cls._instance = super(AlarmController, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """
        Initialize the AlarmController with a logger and an Alarm instance.

        :return: None
        """
        self.logger: Logger = Logger("AlarmControl")
        self.alarm: Alarm = Alarm()

    def activate_alarm(self) -> None:
        """
        Activate the alarm if it is not already active.

        :return: None
        """
        if not self.alarm.active:
            self.logger.log("Activating alarm.", LogLevel.INFO)
            self.alarm.active = True
        else:
            self.logger.log("Alarm is already active.", LogLevel.WARNING)

    def deactivate_alarm(self) -> None:
        """
        Deactivate the alarm if it is currently active.

        :return: None
        """
        if self.alarm.active:
            self.logger.log("Deactivating alarm.", LogLevel.INFO)
            self.alarm.active = False
        else:
            self.logger.log("Alarm is already inactive.", LogLevel.WARNING)

    def is_alarming(self) -> bool:
        """
        Check if the alarm is currently active.

        :return: True if the alarm is active, False otherwise.
        :rtype: bool
        """
        return self.alarm.active
