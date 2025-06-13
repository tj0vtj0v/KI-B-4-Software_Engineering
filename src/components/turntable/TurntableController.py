from src.components.turntable.Turntable import Turntable
from src.helper.Logger import Logger
from src.helper.config import TURNTABLE_STEP_IN_ROTATIONS_PER_MINUTE, TURNTABLE_MIN_ROTATIONS_PER_MINUTE, \
    TURNTABLE_MAX_ROTATIONS_PER_MINUTE
from src.helper.logging.LogLevel import LogLevel


class TurntableController:
    """
    Singleton controller class for managing the turntable's speed and state.

    This class provides methods to update the turntable's speed, set a target speed,
    stop the turntable, and perform an emergency stop. It ensures that only one instance
    of the controller exists throughout the application.
    """
    _instance: 'TurntableController' = None

    def __new__(cls) -> 'TurntableController':
        """
        Create or return the singleton instance of TurntableController.

        :return: The singleton instance of TurntableController.
        :rtype: TurntableController
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """
        Initialize the TurntableController instance.

        Sets up the logger, the turntable object, and initializes the target speed.
        """
        self.logger: Logger = Logger("TurntableControl")
        self.turntable: Turntable = Turntable()
        self.target_rotations_per_minute: float = 0.0

    def update(self) -> None:
        """
        Update the turntable's speed towards the target speed.

        Gradually adjusts the turntable's speed in steps until it matches the target speed.
        """
        self.logger.log("Updating Turntable", LogLevel.DEBUG)

        if self.turntable.rotations_per_minute != self.target_rotations_per_minute:
            if (abs(self.target_rotations_per_minute - self.turntable.rotations_per_minute)
                    <= TURNTABLE_STEP_IN_ROTATIONS_PER_MINUTE):
                self.turntable.rotations_per_minute = self.target_rotations_per_minute
            else:
                if self.target_rotations_per_minute > self.turntable.rotations_per_minute:
                    self.turntable.rotations_per_minute += TURNTABLE_STEP_IN_ROTATIONS_PER_MINUTE
                else:
                    self.turntable.rotations_per_minute -= TURNTABLE_STEP_IN_ROTATIONS_PER_MINUTE

    def set_speed(self, rotations_per_minute: float) -> None:
        """
        Set the target speed for the turntable.

        :param rotations_per_minute: The desired speed in rotations per minute.
        :type rotations_per_minute: float
        :raises ValueError: If the speed is outside the allowed range.
        :return: None
        """
        if (rotations_per_minute < TURNTABLE_MIN_ROTATIONS_PER_MINUTE
                or rotations_per_minute > TURNTABLE_MAX_ROTATIONS_PER_MINUTE):
            raise ValueError("Rotations per minute must be between -5 and 5.")

        if rotations_per_minute == self.target_rotations_per_minute:
            return

        self.target_rotations_per_minute = rotations_per_minute
        self.logger.log(f"Changing the target_speed to {rotations_per_minute}.", LogLevel.INFO)

    def stop(self) -> None:
        """
        Stop the turntable by setting its speed to zero.

        :return: None
        """
        self.set_speed(0)
        self.logger.log("Stopping turntable.", LogLevel.INFO)

    def emergency_stop(self) -> None:
        """
        Immediately stop the turntable and reset the target speed.

        :return: None
        """
        self.turntable.rotations_per_minute = 0.0
        self.target_rotations_per_minute = 0.0
        self.logger.log("Emergency stopping turntable controller.", LogLevel.INFO)
