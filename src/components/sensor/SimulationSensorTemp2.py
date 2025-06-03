import random

from src.components.door.Door import Door
from src.components.magnetron.Magnetron import Magnetron
from src.components.sensor.SimulationSensor import SimulationSensor
from src.helper.config import AMBIENT_TEMPERATURE_IN_CELSIUS


class SimulationSensorTemp2(SimulationSensor):
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.magnetron = Magnetron()
        self.door = Door()
        self.temperature = AMBIENT_TEMPERATURE_IN_CELSIUS

    def get(self) -> float:
        return self.temperature

    def update(self) -> None:
        if self.magnetron.active:
            self.temperature += 0.1
        else:
            self.temperature -= 0.02

        if self.door.opened:
            self.temperature -= 0.1

        self.temperature = max(AMBIENT_TEMPERATURE_IN_CELSIUS, self.temperature)
        self.temperature += random.uniform(-0.01, 0.01)

    def reset(self):
        self.temperature = AMBIENT_TEMPERATURE_IN_CELSIUS
