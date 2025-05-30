import threading
import time

from src.emergency.EmergencyHandler import EmergencyHandler
from src.helper.config import MAIN_LOOP_TIMEOUT_IN_SECONDS, DEFAULT_LOG_LEVEL
from src.helper.Logger import Logger, LogLevel
from src.program.MockProgramController import MockProgramController
from src.user.MockUserInteractionHandler import MockUserInteractionHandler


class SystemControl:
    class State:
        IDLE = "IDLE"
        RUNNING = "RUNNING"
        EMERGENCY = "EMERGENCY"

    def __init__(
            self,
            logger=None,
            emergency_handler=None,
            user_interaction_handler=None,
            program_controller=None
    ):
        self.state = self.State.IDLE
        self.logger = logger or Logger("SystemControl", DEFAULT_LOG_LEVEL)
        self.emergency_handler = emergency_handler or EmergencyHandler()
        self.user_interaction_handler = user_interaction_handler or MockUserInteractionHandler()
        self.program_controller = program_controller or MockProgramController()

    def factory_reset(self):
        self.logger.log("Performing factory reset.")

        self.__init__()

    def declare_emergency(self):
        if self.state != self.State.EMERGENCY:
            self.logger.log("Declaring emergency state.")

            self.state = self.State.EMERGENCY

        else:
            self.logger.log("System is already in emergency state.")

    def shutdown(self):
        if self.state == self.State.IDLE:
            self.logger.log("System is already idle, nothing to shut down.")
        else:
            self.logger.log("Shutting down system.")

            self.program_controller.stop()
            self.state = self.State.IDLE

    def start(self):
        if self.state == self.State.IDLE:
            self.state = self.State.RUNNING
            self.program_controller.start()

            threading.Thread(target=self.loop, daemon=True).start()

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
