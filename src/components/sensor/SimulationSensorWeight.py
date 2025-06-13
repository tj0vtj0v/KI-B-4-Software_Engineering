import random

from src.components.door.Door import Door
from src.components.sensor.SimulationSensor import SimulationSensor
from src.helper.config import TURNTABLE_WEIGHT_IN_GRAMS


class SimulationSensorWeight(SimulationSensor):
    """
    Singleton class that simulates a weight sensor for a turntable.

    This class tracks the weight on the turntable and updates it based on door state and random fluctuations.
    """

    _instance: 'SimulationSensorWeight' = None

    def __new__(cls) -> 'SimulationSensorWeight':
        """
        Create or return the singleton instance of SimulationSensorWeight.

        :return: The singleton instance of SimulationSensorWeight.
        :rtype: SimulationSensorWeight
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """
        Initialize the SimulationSensorWeight instance.

        Sets up the door sensor, last door state, and initial weight.
        """
        self.door: Door = Door()
        self.last_door_opened: bool = False
        self.weight: float = TURNTABLE_WEIGHT_IN_GRAMS

    def get(self) -> float:
        """
        Get the current weight measured by the sensor.

        :return: The current weight in grams.
        :rtype: float
        """
        return self.weight

    def update(self) -> None:
        """
        Update the sensor's weight value.

        Increases the weight if the door has just been opened and adds a small random fluctuation.
        """
        if self.door.opened and not self.last_door_opened:
            self.weight += 530

        self.last_door_opened = self.door.opened
        self.weight += random.uniform(-0.1, 0.1)

    def reset(self) -> None:
        """
        Reset the sensor's weight to the initial value.

        :return: None
        """
        self.weight = TURNTABLE_WEIGHT_IN_GRAMS
