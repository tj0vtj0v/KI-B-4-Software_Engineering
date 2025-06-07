from src.components.turntable.Turntable import Turntable
from src.helper.config import TURNTABLE_STEP_IN_ROTATIONS_PER_MINUTE, TURNTABLE_MIN_ROTATIONS_PER_MINUTE, \
    TURNTABLE_MAX_ROTATIONS_PER_MINUTE


class TurntableController:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.turntable = Turntable()
        self.target_rotations_per_minute = 0.0

    def update(self):
        if self.turntable.rotations_per_minute != self.target_rotations_per_minute:
            if (abs(self.target_rotations_per_minute - self.turntable.rotations_per_minute)
                    <= TURNTABLE_STEP_IN_ROTATIONS_PER_MINUTE):
                self.turntable.rotations_per_minute = self.target_rotations_per_minute
            else:
                if self.target_rotations_per_minute > self.turntable.rotations_per_minute:
                    self.turntable.rotations_per_minute += TURNTABLE_STEP_IN_ROTATIONS_PER_MINUTE
                else:
                    self.turntable.rotations_per_minute -= TURNTABLE_STEP_IN_ROTATIONS_PER_MINUTE

    def set_speed(self, rotations_per_minute: float):
        if (rotations_per_minute < TURNTABLE_MIN_ROTATIONS_PER_MINUTE
                or rotations_per_minute > TURNTABLE_MAX_ROTATIONS_PER_MINUTE):
            raise ValueError("Rotations per minute must be between -5 and 5.")

        self.target_rotations_per_minute = rotations_per_minute

    def stop(self):
        self.set_speed(0)

    def emergency_stop(self):
        self.turntable.rotations_per_minute = 0.0
        self.target_rotations_per_minute = 0.0
