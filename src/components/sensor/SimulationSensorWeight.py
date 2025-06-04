import random

from src.components.door.Door import Door
from src.components.sensor.SimulationSensor import SimulationSensor
from src.helper.config import TURNTABLE_WEIGHT_IN_GRAMS


class SimulationSensorWeight(SimulationSensor):
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.door = Door()
        self.last_door_opened = False

        self.weight = TURNTABLE_WEIGHT_IN_GRAMS

    def get(self) -> float:
        return self.weight

    def update(self) -> None:
        if self.door.opened and not self.last_door_opened:
            self.weight += 530

        self.last_door_opened = self.door.opened
        self.weight += random.uniform(-0.1, 0.1)

    def reset(self):
        self.weight = TURNTABLE_WEIGHT_IN_GRAMS
