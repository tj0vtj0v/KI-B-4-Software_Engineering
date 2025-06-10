from __future__ import annotations

from typing import TYPE_CHECKING

from src.helper.Logger import Logger, LogLevel
from src.helper.exceptions import CustomException, MockException, DoorException, ProgramAlreadyRunningException

if TYPE_CHECKING:
    from src.SystemControl import SystemControl


class EmergencyHandler:
    error: CustomException | None = None
    logger = Logger("EmergencyHandler")

    @classmethod
    def observe(cls, func):
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)

            except CustomException as e:
                cls.logger.log("Internal error occurred, entering emergency state.", LogLevel.ERROR)
                self.declare_emergency()
                cls.error = e

            except Exception as e:
                cls.logger.log(f"Major error ({e}) occurred, shutting down.", LogLevel.CRITICAL)
                raise e

        return wrapper

    @classmethod
    def is_busy(cls):
        return cls.error is not None

    def handle_emergency(self, system_control: "SystemControl"):
        system_control.alarm_controller.deactivate_alarm()

        if isinstance(self.error, MockException):
            self.logger.log("Mock exception occurred, simulating emergency handling.", LogLevel.ERROR)
            EmergencyHandler.error = None

            return

        if isinstance(self.error, DoorException):
            self.logger.log("Door exception occurred, stopping the running program.", LogLevel.ERROR)
            system_control.emergency_stop_program()
            EmergencyHandler.error = None

            return

        if isinstance(self.error, ProgramAlreadyRunningException):
            self.logger.log("A Program already running.", LogLevel.ERROR)
            EmergencyHandler.error = None

            return

        self.logger.log("Resetting system.", LogLevel.ERROR)
        system_control.stop()
        system_control.factory_reset()

        # For real errors, the handling will be added later
