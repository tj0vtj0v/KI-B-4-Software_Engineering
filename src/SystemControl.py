import threading
import time

from src.components.alarm.AlarmController import AlarmController
from src.components.sensor.SensorManager import SensorManager
from src.emergency.EmergencyHandler import EmergencyHandler
from src.helper.Logger import Logger, LogLevel
from src.helper.config import MAIN_LOOP_TIMEOUT_IN_SECONDS, DEFAULT_LOG_LEVEL
from src.program.MockProgramController import MockProgramController
from src.user.MockUserInteractionHandler import MockUserInteractionHandler


class SystemControl:
    class State:
        IDLE = "IDLE"
        RUNNING = "RUNNING"
        EMERGENCY = "EMERGENCY"

    def __init__(self, ):
        self.state = self.State.IDLE

        self.logger = Logger("SystemControl")
        self.emergency_handler = EmergencyHandler()
        self.alarm_controller = AlarmController()
        self.user_interaction_handler = MockUserInteractionHandler()
        self.program_controller = MockProgramController()
        self.sensor_manager = SensorManager()

    def factory_reset(self):
        self.logger.log("Performing factory reset.")

        self.__init__()

    def declare_emergency(self):
        if self.state != self.State.EMERGENCY:
            self.logger.log("Declaring emergency state.")

            if not self.alarm_controller.is_alarming():
                self.alarm_controller.activate_alarm()
            self.state = self.State.EMERGENCY

        else:
            self.logger.log("System is already in emergency state.")

    def stop(self):
        if self.state == self.State.IDLE:
            self.logger.log("System is already idle, nothing to shut down.")
        else:
            self.logger.log("Shutting down system.")

            self.sensor_manager.reset()
            self.program_controller.stop()
            self.state = self.State.IDLE

    def start(self):
        if self.state == self.State.IDLE:
            self.state = self.State.RUNNING
            self.program_controller.start()

            threading.Thread(target=self.loop).start()

            self.logger.log("System started.")
        else:
            self.logger.log("System is already running or in emergency state.", level=LogLevel.WARNING)

    def loop(self):
        while True:
            time.sleep(MAIN_LOOP_TIMEOUT_IN_SECONDS)

            match self.state:
                case self.State.IDLE:
                    self.logger.log("System is idle.")
                    break  # TODO build a watchdog to wake up

                case self.State.RUNNING:
                    self.logger.log("System is running.")

                    self.loop_action()

                case self.State.EMERGENCY:
                    self.logger.log("Emergency state!", level=LogLevel.WARNING)

                    if self.emergency_handler.is_busy():
                        self.emergency_handler.handle_emergency(self)
                    else:
                        self.logger.log("No error to handle, exiting emergency state.")

                        self.state = self.State.RUNNING

    @EmergencyHandler.observe
    def loop_action(self):
        self.user_interaction_handler.get_interactions()

        self.program_controller.update()

        self.user_interaction_handler.update_display()
        self.sensor_manager.update_sensors()
