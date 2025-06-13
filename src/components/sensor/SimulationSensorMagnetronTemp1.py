import random

from src.components.cooling.CoolingFan import CoolingFan
from src.components.magnetron.Magnetron import Magnetron
from src.components.sensor.SimulationSensor import SimulationSensor
from src.helper.config import AMBIENT_TEMPERATURE_IN_CELSIUS


class SimulationSensorMagnetronTemp1(SimulationSensor):
    """
    Singleton simulation sensor for monitoring the magnetron temperature.

    This class simulates the temperature of a magnetron, factoring in the
    effects of the magnetron's activity, a cooling fan, and random noise.
    """

    _instance: "SimulationSensorMagnetronTemp1" = None

    def __new__(cls) -> "SimulationSensorMagnetronTemp1":
        """
        Create or return the singleton instance of the class.

        :return: The singleton instance of SimulationSensorMagnetronTemp1.
        :rtype: SimulationSensorMagnetronTemp1
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """
        Initialize the simulation sensor with default values.
        """
        self.magnetron: Magnetron = Magnetron()
        self.cooling_fan: CoolingFan = CoolingFan()
        self.temperature: float = AMBIENT_TEMPERATURE_IN_CELSIUS

    def get(self) -> float:
        """
        Get the current simulated temperature.

        :return: The current temperature in Celsius.
        :rtype: float
        """
        return self.temperature

    def update(self) -> None:
        """
        Update the simulated temperature based on the magnetron state,
        cooling fan power, and random noise.

        :return: None
        """
        if self.magnetron.active:
            self.temperature += 0.3
        else:
            self.temperature -= 0.05

        self.temperature -= 0.4 * self.cooling_fan.power_share

        self.temperature = max(AMBIENT_TEMPERATURE_IN_CELSIUS, self.temperature)
        self.temperature += random.uniform(-0.01, 0.01)

    def reset(self) -> None:
        """
        Reset the simulated temperature to the ambient value.

        :return: None
        """
        self.temperature = AMBIENT_TEMPERATURE_IN_CELSIUS
