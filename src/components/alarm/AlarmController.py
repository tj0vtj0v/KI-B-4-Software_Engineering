from src.components.alarm.Alarm import Alarm
from src.helper.Logger import Logger
from src.helper.logging.LogLevel import LogLevel


class AlarmController:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AlarmController, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.logger = Logger("AlarmControl")
        self.alarm = Alarm()

    def activate_alarm(self):
        if not self.alarm.active:
            self.logger.log("Activating alarm.", level=LogLevel.INFO)
            self.alarm.active = True
        else:
            self.logger.log("Alarm is already active.", level=LogLevel.WARNING)

    def deactivate_alarm(self):
        if self.alarm.active:
            self.logger.log("Deactivating alarm.", level=LogLevel.INFO)
            self.alarm.active = False
        else:
            self.logger.log("Alarm is already inactive.", level=LogLevel.WARNING)

    def is_alarming(self) -> bool:
        return self.alarm.active
