from src.components.cooling.CoolingFan import CoolingFan
from src.components.sensor.SensorManager import SensorManager
from src.helper.config import COOLING_FAN_STEP_IN_PERCENT


class CoolingFanController:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.cooling_fan = CoolingFan()
        self.sensors = SensorManager()
        self.target_power_share = 0.0

    def set_target_power_share(self, power_share):
        self.target_power_share = power_share

    @staticmethod
    def magnetron_temp_to_power_share(magnetron_temp: float) -> float:
        if magnetron_temp <= 50.0:
            return 0.0
        elif magnetron_temp <= 100.0:
            return (magnetron_temp - 50.0) / 200.0
        elif magnetron_temp < 150.0:
            return 0.25 + (magnetron_temp - 100.0) * 0.015
        else:
            return 1.0

    def update(self):
        magnetron_temp = (self.sensors.magnetron_temp1() + self.sensors.magnetron_temp2()) / 2.0

        if self.target_power_share < self.magnetron_temp_to_power_share(magnetron_temp):
            self.target_power_share = self.magnetron_temp_to_power_share(magnetron_temp)

        if self.cooling_fan.power_share != self.target_power_share:
            if abs(self.target_power_share - self.cooling_fan.power_share) <= COOLING_FAN_STEP_IN_PERCENT:
                self.cooling_fan.power_share = self.target_power_share
            else:
                if self.target_power_share > self.cooling_fan.power_share:
                    self.cooling_fan.power_share += COOLING_FAN_STEP_IN_PERCENT
                else:
                    self.cooling_fan.power_share -= COOLING_FAN_STEP_IN_PERCENT

        self.cooling_fan.power_share = max(0.0, min(self.cooling_fan.power_share, 1.0))

    def start(self):
        self.target_power_share = 0.2

    def stop(self):
        self.target_power_share = 0.0
