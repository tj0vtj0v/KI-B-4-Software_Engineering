from src.components.reflector.Reflector import Reflector
from src.helper.config import REFLECTOR_STEP_IN_DEGREES, REFLECTOR_MIN_ANGLE_IN_DEGREES, REFLECTOR_MAX_ANGLE_IN_DEGREES


class ReflectorController:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.reflector = Reflector()
        self.target_angle = 0.0

    def update(self):
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

        self.target_angle = angle

    def stop(self):
        self.set_angle(0.0)

    def emergency_stop(self):
        self.target_angle = self.reflector.angle
