import threading
import time

from src.components.alarm.AlarmController import AlarmController
from src.components.sensor.SensorManager import SensorManager
from src.emergency.EmergencyHandler import EmergencyHandler
from src.helper.Action import Action
from src.helper.Logger import Logger, LogLevel
from src.helper.config import MAIN_LOOP_TIMEOUT_IN_SECONDS
from src.helper.exceptions import ProgramAlreadyRunningException
from src.program.ProgramController import ProgramController
from src.user.MockUserInteractionHandler import MockUserInteractionHandler


class SystemControl:
    class State:
        IDLE = "IDLE"
        RUNNING = "RUNNING"
        EMERGENCY = "EMERGENCY"

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SystemControl, cls).__new__(cls)
        return cls._instance

    def __init__(self, ):
        self.state = self.State.IDLE

        self.logger = Logger("SystemControl")
        self.emergency_handler = EmergencyHandler()
        self.alarm_controller = AlarmController()
        self.user_interaction_handler = MockUserInteractionHandler()
        self.program_controller = ProgramController()
        self.sensor_manager = SensorManager()

    def factory_reset(self):
        self.logger.log("Performing factory reset", LogLevel.INFO)

        self.__init__()

    def declare_emergency(self):
        if self.state != self.State.EMERGENCY:
            self.logger.log("Declaring emergency state", LogLevel.INFO)

            if not self.alarm_controller.is_alarming():
                self.alarm_controller.activate_alarm()
            self.state = self.State.EMERGENCY

        else:
            self.logger.log("System is already in emergency state", LogLevel.WARNING)

    def stop(self):
        if self.state == self.State.IDLE:
            self.logger.log("System is already idle, nothing to shut down", LogLevel.WARNING)
        else:
            self.logger.log("Shutting down system", LogLevel.INFO)

            self.sensor_manager.reset()
            self.program_controller.stop()
            self.state = self.State.IDLE

    def start(self):
        if self.state == self.State.IDLE:
            self.state = self.State.RUNNING

            threading.Thread(target=self.loop).start()

            self.logger.log("System started", LogLevel.INFO)
        else:
            self.logger.log("System is already running or in emergency state.", LogLevel.WARNING)

    def loop(self):
        while True:
            time.sleep(MAIN_LOOP_TIMEOUT_IN_SECONDS)

            match self.state:
                case self.State.IDLE:
                    self.logger.log("System is idle", LogLevel.INFO)
                    break  # TODO build a watchdog to wake up

                case self.State.RUNNING:
                    self.logger.log("System is running", LogLevel.DEBUG)

                    self.loop_action()

                case self.State.EMERGENCY:
                    self.logger.log("Emergency state!", LogLevel.WARNING)

                    if self.emergency_handler.is_busy():
                        self.emergency_handler.handle_emergency(self)
                    else:
                        self.logger.log("No error to handle, exiting emergency state", LogLevel.INFO)

                        self.state = self.State.RUNNING

    @EmergencyHandler.observe
    def loop_action(self):
        action, program = self.user_interaction_handler.get_interactions()

        if action is not None:
            match action:
                case Action.START:
                    if not self.program_controller.is_running():
                        self.program_controller.start(program)
                    else:
                        raise ProgramAlreadyRunningException()

                case Action.STOP:
                    if self.program_controller.is_running():
                        self.program_controller.stop()
                    else:
                        self.logger.log("No program running, nothing to stop", LogLevel.INFO)

                case Action.PAUSE:
                    if self.program_controller.is_running() and not self.program_controller.is_paused():
                        self.program_controller.pause()
                    else:
                        self.logger.log("No program running, nothing to pause", LogLevel.INFO)

                case Action.RESUME:
                    if self.program_controller.is_running() and self.program_controller.is_paused():
                        self.program_controller.resume()
                    else:
                        self.logger.log("No running program paused, nothing to resume", LogLevel.INFO)

        self.user_interaction_handler.update_display(*self.program_controller.get_state_tupel())
        self.sensor_manager.update_sensors()

    def emergency_stop_program(self):
        self.logger.log("Emergency stopping the program", LogLevel.INFO)
        self.program_controller.emergency_stop()
