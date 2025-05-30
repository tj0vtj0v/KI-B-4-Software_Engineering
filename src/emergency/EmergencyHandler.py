from __future__ import annotations

from src.helper.exceptions import CustomException, MockException
from src.helper.Logger import Logger, LogLevel
from src.helper.config import DEFAULT_LOG_LEVEL


class EmergencyHandler:
    error: CustomException | None = None
    logger = Logger("EmergencyHandler", DEFAULT_LOG_LEVEL)

    @classmethod
    def observe(cls, func):
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)

            except CustomException as e:
                cls.logger.log("Internal error occurred, entering emergency state.", level=LogLevel.ERROR)
                self.declare_emergency()
                cls.error = e

            except Exception as e:
                cls.logger.log(f"Major error ({e}) occurred, shutting down.", level=LogLevel.CRITICAL)
                self.shutdown()

        return wrapper

    @classmethod
    def is_busy(cls):
        return cls.error is not None

    def handle_emergency(self, system_control: "SystemControl"):
        if isinstance(self.error, MockException):
            self.logger.log("Mock exception occurred, simulating emergency handling.", level=LogLevel.ERROR)
            EmergencyHandler.error = None

            return

        self.logger.log("Resetting system.", level=LogLevel.ERROR)
        system_control.factory_reset()

        # For real errors, the handling will be added later
