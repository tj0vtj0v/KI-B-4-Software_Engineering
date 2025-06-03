import unittest

from src.components.sensor.SimulationSensor import SimulationSensor


class TestSimulationSensor(unittest.TestCase):
    def test_get__not_implemented__raises_not_implemented_error(self):
        sensor = SimulationSensor()
        with self.assertRaises(NotImplementedError):
            sensor.get()

    def test_update__not_implemented__raises_not_implemented_error(self):
        sensor = SimulationSensor()
        with self.assertRaises(NotImplementedError):
            sensor.update()

    def test_reset__not_implemented__raises_not_implemented_error(self):
        sensor = SimulationSensor()
        with self.assertRaises(NotImplementedError):
            sensor.reset()
