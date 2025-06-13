from src.components.reflector.Reflector import Reflector
from src.helper.Logger import Logger
from src.helper.config import REFLECTOR_STEP_IN_DEGREES, REFLECTOR_MIN_ANGLE_IN_DEGREES, REFLECTOR_MAX_ANGLE_IN_DEGREES
from src.helper.logging.LogLevel import LogLevel


class ReflectorController:
    """
    Singleton controller for managing the reflector's angle and state.

    This class provides methods to update the reflector's angle, set a target angle,
    stop the reflector, and perform an emergency stop. It ensures the angle remains
    within defined bounds and logs all actions.
    """

    _instance: "ReflectorController" = None

    def __new__(cls) -> "ReflectorController":
        """
        Create or return the singleton instance of ReflectorController.

        :return: The singleton instance of ReflectorController.
        :rtype: ReflectorController
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """
        Initialize the ReflectorController with a logger, reflector, and default target angle.

        :return: None
        """
        self.logger: Logger = Logger("ReflectorControl")
        self.reflector: Reflector = Reflector()
        self.target_angle: float = 0.0

    def update(self) -> None:
        """
        Update the reflector's angle towards the target angle in steps.

        Ensures the angle does not exceed the minimum or maximum allowed values.
        Logs the update process.

        :return: None
        """
        self.logger.log("Updating Reflector", LogLevel.DEBUG)

        if self.reflector.angle != self.target_angle:
            if abs(self.target_angle - self.reflector.angle) <= REFLECTOR_STEP_IN_DEGREES:
                self.reflector.angle = self.target_angle
            else:
                if self.target_angle > self.reflector.angle:
                    self.reflector.angle += REFLECTOR_STEP_IN_DEGREES
                else:
                    self.reflector.angle -= REFLECTOR_STEP_IN_DEGREES

        self.reflector.angle = max(
            REFLECTOR_MIN_ANGLE_IN_DEGREES,
            min(REFLECTOR_MAX_ANGLE_IN_DEGREES, self.reflector.angle)
        )

    def set_angle(self, angle: float) -> None:
        """
        Set a new target angle for the reflector.

        :param angle: The desired target angle in degrees.
        :type angle: float
        :raises ValueError: If the angle is outside the allowed range.
        :return: None
        """
        if angle < REFLECTOR_MIN_ANGLE_IN_DEGREES or angle > REFLECTOR_MAX_ANGLE_IN_DEGREES:
            raise ValueError(
                f"Angle must be between {REFLECTOR_MIN_ANGLE_IN_DEGREES} and {REFLECTOR_MAX_ANGLE_IN_DEGREES} degrees."
            )

        if angle == self.target_angle:
            return

        self.target_angle = angle
        self.logger.info(f"Changing the reflector target_angle to {angle}.", LogLevel.INFO)

    def stop(self) -> None:
        """
        Stop the reflector by setting its target angle to 0.0.

        Logs the stop action.

        :return: None
        """
        self.set_angle(0.0)
        self.logger.log("Stopping reflector controller.", LogLevel.INFO)

    def emergency_stop(self) -> None:
        """
        Immediately stop the reflector by setting the target angle to the current angle.

        Logs the emergency stop action.

        :return: None
        """
        self.target_angle = self.reflector.angle
        self.logger.log("Emergency stopping reflector controller.", LogLevel.INFO)
