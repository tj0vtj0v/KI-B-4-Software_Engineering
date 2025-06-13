import random

from src.components.door.Door import Door
from src.components.magnetron.Magnetron import Magnetron
from src.components.sensor.SimulationSensor import SimulationSensor
from src.helper.config import AMBIENT_TEMPERATURE_IN_CELSIUS


class SimulationSensorTemp1(SimulationSensor):
    """
    Singleton simulation sensor for temperature, emulating a microwave's temperature sensor.

    This class simulates temperature changes based on the state of the magnetron and door.
    """

    _instance: "SimulationSensorTemp1" = None

    def __new__(cls) -> "SimulationSensorTemp1":
        """
        Create or return the singleton instance of SimulationSensorTemp1.

        :return: The singleton instance of SimulationSensorTemp1.
        :rtype: SimulationSensorTemp1
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """
        Initialize the SimulationSensorTemp1 instance.

        :return: None
        """
        self.magnetron: Magnetron = Magnetron()
        self.door: Door = Door()
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
        Update the simulated temperature based on the magnetron and door states.

        :return: None
        """
        if self.magnetron.active:
            self.temperature += 0.1
        else:
            self.temperature -= 0.02

        if self.door.opened:
            self.temperature -= 0.1

        self.temperature = max(AMBIENT_TEMPERATURE_IN_CELSIUS, self.temperature)
        self.temperature += random.uniform(-0.01, 0.01)

    def reset(self) -> None:
        """
        Reset the simulated temperature to the ambient value.

        :return: None
        """
        self.temperature = AMBIENT_TEMPERATURE_IN_CELSIUS
