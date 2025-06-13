import random

from src.components.door.Door import Door
from src.components.magnetron.Magnetron import Magnetron
from src.components.sensor.SimulationSensor import SimulationSensor
from src.helper.config import AMBIENT_HUMIDITY_IN_PERCENT


class SimulationSensorHumidity(SimulationSensor):
    """
    Singleton class that simulates a humidity sensor for a microwave environment.

    The sensor updates its humidity value based on the state of the magnetron and door,
    and introduces small random fluctuations to simulate real-world sensor noise.
    """

    _instance: "SimulationSensorHumidity" = None

    def __new__(cls) -> "SimulationSensorHumidity":
        """
        Create or return the singleton instance of SimulationSensorHumidity.

        :return: The singleton instance of SimulationSensorHumidity.
        :rtype: SimulationSensorHumidity
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """
        Initialize the SimulationSensorHumidity instance.

        Sets up the magnetron, door, and initial humidity value.
        """
        self.magnetron: Magnetron = Magnetron()
        self.door: Door = Door()
        self.humidity: float = AMBIENT_HUMIDITY_IN_PERCENT

    def get(self) -> float:
        """
        Get the current humidity value.

        :return: The current humidity in percent.
        :rtype: float
        """
        return self.humidity

    def update(self) -> None:
        """
        Update the humidity value based on the state of the magnetron and door.

        - Increases humidity if the magnetron is active.
        - Decreases humidity if the magnetron is inactive or the door is open.
        - Ensures humidity does not fall below the ambient value.
        - Adds a small random fluctuation to simulate sensor noise.

        :return: None
        """
        if self.magnetron.active:
            self.humidity += 0.1
        else:
            self.humidity -= 0.02

        if self.door.opened:
            self.humidity -= 0.1

        self.humidity = max(AMBIENT_HUMIDITY_IN_PERCENT, self.humidity)
        self.humidity += random.uniform(-0.01, 0.01)

    def reset(self) -> None:
        """
        Reset the humidity value to the ambient humidity.

        :return: None
        """
        self.humidity = AMBIENT_HUMIDITY_IN_PERCENT
