import random

from src.components.door.Door import Door
from src.components.magnetron.Magnetron import Magnetron
from src.components.sensor.SimulationSensor import SimulationSensor
from src.helper.config import AMBIENT_HUMIDITY_IN_PERCENT


class SimulationSensorHumidity(SimulationSensor):
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.magnetron = Magnetron()
        self.door = Door()
        self.humidity = AMBIENT_HUMIDITY_IN_PERCENT

    def get(self) -> float:
        return self.humidity

    def update(self) -> None:
        if self.magnetron.active:
            self.humidity += 0.1
        else:
            self.humidity -= 0.02

        if self.door.opened:
            self.humidity -= 0.1

        self.humidity = max(AMBIENT_HUMIDITY_IN_PERCENT, self.humidity)
        self.humidity += random.uniform(-0.01, 0.01)

    def reset(self):
        self.humidity = AMBIENT_HUMIDITY_IN_PERCENT
