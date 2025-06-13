import random

from src.components.door.Door import Door
from src.components.magnetron.Magnetron import Magnetron
from src.components.sensor.SimulationSensor import SimulationSensor
from src.helper.config import AMBIENT_TEMPERATURE_IN_CELSIUS


class SimulationSensorTemp2(SimulationSensor):
    """
    Singleton simulation sensor for temperature, emulating temperature changes
    based on the state of the magnetron and door.

    Attributes
    ----------
    magnetron : Magnetron
        Instance of the Magnetron component.
    door : Door
        Instance of the Door component.
    temperature : float
        Current simulated temperature in Celsius.
    """

    _instance: 'SimulationSensorTemp2' = None

    def __new__(cls) -> 'SimulationSensorTemp2':
        """
        Ensures only one instance of SimulationSensorTemp2 exists.

        :return: The singleton instance of SimulationSensorTemp2.
        :rtype: SimulationSensorTemp2
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """
        Initializes the SimulationSensorTemp2 instance with default values.
        """
        self.magnetron: Magnetron = Magnetron()
        self.door: Door = Door()
        self.temperature: float = AMBIENT_TEMPERATURE_IN_CELSIUS

    def get(self) -> float:
        """
        Retrieves the current simulated temperature.

        :return: The current temperature in Celsius.
        :rtype: float
        """
        return self.temperature

    def update(self) -> None:
        """
        Updates the simulated temperature based on the state of the magnetron and door.
        Increases temperature if the magnetron is active, decreases if not.
        Further decreases if the door is open. Adds a small random fluctuation.
        Ensures temperature does not fall below ambient.
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
        Resets the simulated temperature to the ambient value.
        """
        self.temperature = AMBIENT_TEMPERATURE_IN_CELSIUS
