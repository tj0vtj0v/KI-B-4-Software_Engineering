import random

from src.components.cooling.CoolingFan import CoolingFan
from src.components.magnetron.Magnetron import Magnetron
from src.components.sensor.SimulationSensor import SimulationSensor
from src.helper.config import AMBIENT_TEMPERATURE_IN_CELSIUS


class SimulationSensorMagnetronTemp2(SimulationSensor):
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.magnetron = Magnetron()
        self.cooling_fan = CoolingFan()
        self.temperature = AMBIENT_TEMPERATURE_IN_CELSIUS

    def get(self) -> float:
        return self.temperature

    def update(self) -> None:
        if self.magnetron.active:
            self.temperature += 0.3
        else:
            self.temperature -= 0.05

        self.temperature -= 0.4 * self.cooling_fan.power_share

        self.temperature = max(AMBIENT_TEMPERATURE_IN_CELSIUS, self.temperature)
        self.temperature += random.uniform(-0.01, 0.01)

    def reset(self):
        self.temperature = AMBIENT_TEMPERATURE_IN_CELSIUS
