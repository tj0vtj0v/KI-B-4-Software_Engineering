from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Any

from src.helper.Logger import Logger, LogLevel
from src.helper.exceptions import CustomException, MockException, DoorException, ProgramAlreadyRunningException

if TYPE_CHECKING:
    from src.SystemControl import SystemControl


class EmergencyHandler:
    """
    Singleton class responsible for handling emergency situations in the system.

    Attributes
    ----------
    error : CustomException | None
        Stores the current error that triggered the emergency state.
    logger : Logger
        Logger instance for logging emergency events.
    _instance : EmergencyHandler | None
        Singleton instance of the EmergencyHandler.
    """

    error: CustomException | None = None
    logger: Logger = Logger("EmergencyHandler")
    _instance: EmergencyHandler | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> EmergencyHandler:
        """
        Ensures only one instance of EmergencyHandler exists (Singleton pattern).

        :param args: Positional arguments.
        :param kwargs: Keyword arguments.
        :return: Singleton instance of EmergencyHandler.
        :rtype: EmergencyHandler
        """
        if cls._instance is None:
            cls._instance = super(EmergencyHandler, cls).__new__(cls)
        return cls._instance

    @classmethod
    def observe(cls, func: Callable[..., Any]) -> Callable[..., Any]:
        """
        Decorator to observe and handle exceptions in decorated methods.

        :param func: The function to be wrapped.
        :type func: Callable[..., Any]
        :return: Wrapped function with emergency handling.
        :rtype: Callable[..., Any]
        """

        def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
            """
            Wrapper function to catch and handle exceptions.

            :param self: The instance of the class.
            :param args: Positional arguments for the wrapped function.
            :param kwargs: Keyword arguments for the wrapped function.
            :return: Result of the wrapped function or None if an exception occurs.
            """
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
    def is_busy(cls) -> bool:
        """
        Checks if the EmergencyHandler is currently handling an error.

        :return: True if an error is being handled, False otherwise.
        :rtype: bool
        """
        return cls.error is not None

    def handle_emergency(self, system_control: "SystemControl") -> None:
        """
        Handles the emergency based on the type of error stored in `self.error`.

        :param system_control: The system control instance to manage system state.
        :type system_control: SystemControl
        :return: None
        """
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
            self.logger.log("A Program is already running.", LogLevel.ERROR)
            EmergencyHandler.error = None
            return

        self.logger.log("Resetting system.", LogLevel.ERROR)
        system_control.stop()
        system_control.factory_reset()

        # For real errors, the handling will be added later
