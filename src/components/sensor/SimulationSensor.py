from abc import ABC


class SimulationSensor(ABC):
    def get(self) -> float:
        """
        Get datapoint of the sensor simulation.
        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def update(self) -> None:
        """
        Update the sensor simulation.
        This method can be overridden by subclasses if needed.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def reset(self) -> None:
        """
        Reset the sensor simulation to its initial state.
        This method can be overridden by subclasses if needed.
        """
        raise NotImplementedError("Subclasses must implement this method.")
