from abc import ABC


class SimulationSensor(ABC):
    def get(self) -> float:
        """
        Get datapoint of the sensor simulation.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def update(self) -> None:
        """
        Update the sensor simulation.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def reset(self) -> None:
        """
        Reset the sensor simulation to its initial state.
        """
        raise NotImplementedError("Subclasses must implement this method.")
