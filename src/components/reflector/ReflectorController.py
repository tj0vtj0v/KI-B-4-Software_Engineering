from src.components.reflector.Reflector import Reflector
from src.helper.Logger import Logger
from src.helper.config import REFLECTOR_STEP_IN_DEGREES, REFLECTOR_MIN_ANGLE_IN_DEGREES, REFLECTOR_MAX_ANGLE_IN_DEGREES
from src.helper.logging.LogLevel import LogLevel


class ReflectorController:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.logger = Logger("ReflectorControl")
        self.reflector = Reflector()
        self.target_angle = 0.0

    def update(self):
        self.logger.log("Updating Reflector", LogLevel.DEBUG)

        if self.reflector.angle != self.target_angle:
            if abs(self.target_angle - self.reflector.angle) <= REFLECTOR_STEP_IN_DEGREES:
                self.reflector.angle = self.target_angle
            else:
                if self.target_angle > self.reflector.angle:
                    self.reflector.angle += REFLECTOR_STEP_IN_DEGREES
                else:
                    self.reflector.angle -= REFLECTOR_STEP_IN_DEGREES

        self.reflector.angle = max(REFLECTOR_MIN_ANGLE_IN_DEGREES,
                                   min(REFLECTOR_MAX_ANGLE_IN_DEGREES, self.reflector.angle)
                                   )

    def set_angle(self, angle: float):
        if angle < REFLECTOR_MIN_ANGLE_IN_DEGREES or angle > REFLECTOR_MAX_ANGLE_IN_DEGREES:
            raise ValueError(
                f"Angle must be between {REFLECTOR_MIN_ANGLE_IN_DEGREES} and {REFLECTOR_MAX_ANGLE_IN_DEGREES} degrees."
            )

        if angle == self.target_angle:
            return

        self.target_angle = angle
        self.logger.info(f"Changing the reflector target_angle to {angle}.", LogLevel.INFO)

    def stop(self):
        self.set_angle(0.0)
        self.logger.log("Stopping reflector controller.", LogLevel.INFO)

    def emergency_stop(self):
        self.target_angle = self.reflector.angle
        self.logger.log("Emergency stopping reflector controller.", LogLevel.INFO)
