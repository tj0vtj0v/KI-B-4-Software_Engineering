from abc import ABC


class SimulationSensor(ABC):
    """
    Abstract base class for a simulation sensor.

    This class defines the interface for sensor simulation, requiring subclasses
    to implement methods for retrieving, updating, and resetting the sensor state.
    """

    def get(self) -> float:
        """
        Get a datapoint from the sensor simulation.

        :return: The current simulated sensor value as a float.
        :rtype: float
        :raises NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def update(self) -> None:
        """
        Update the state of the sensor simulation.

        This method should be implemented by subclasses to advance the simulation state.

        :return: None
        :rtype: None
        :raises NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def reset(self) -> None:
        """
        Reset the sensor simulation to its initial state.

        This method should be implemented by subclasses to restore the simulation to its starting conditions.

        :return: None
        :rtype: None
        :raises NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError("Subclasses must implement this method.")
