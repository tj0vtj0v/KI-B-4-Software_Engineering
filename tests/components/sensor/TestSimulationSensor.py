import unittest

from src.components.sensor.SimulationSensor import SimulationSensor


class TestSimulationSensor(unittest.TestCase):
    def setUp(self):
        self.sensor = SimulationSensor()

    def tearDown(self):
        del self.sensor

    def test_get__not_implemented__raises_not_implemented_error(self):
        with self.assertRaises(NotImplementedError):
            self.sensor.get()

    def test_update__not_implemented__raises_not_implemented_error(self):
        with self.assertRaises(NotImplementedError):
            self.sensor.update()

    def test_reset__not_implemented__raises_not_implemented_error(self):
        with self.assertRaises(NotImplementedError):
            self.sensor.reset()
