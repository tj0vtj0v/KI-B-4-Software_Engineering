import unittest
from unittest.mock import patch

from src.components.sensor.SimulationSensorMagnetronTemp2 import SimulationSensorMagnetronTemp2
from src.helper.config import AMBIENT_TEMPERATURE_IN_CELSIUS


class TestSimulationSensorMagnetronTemp2(unittest.TestCase):
    def setUp(self):
        SimulationSensorMagnetronTemp2._instance = None
        self.sensor = SimulationSensorMagnetronTemp2()

    def test_get__default_temperature__returns_ambient_temperature(self):
        result = self.sensor.get()

        self.assertEqual(result, AMBIENT_TEMPERATURE_IN_CELSIUS)

    @patch('src.components.sensor.SimulationSensorMagnetronTemp2.random.uniform', return_value=0.01)
    def test_update__magnetron_active__increases_temperature(self, mock_random):
        self.sensor.magnetron.active = True
        self.sensor.cooling_fan.power_share = 0
        self.sensor.update()

        self.assertEqual(self.sensor.temperature, AMBIENT_TEMPERATURE_IN_CELSIUS + 0.3 + 0.01)

    @patch('src.components.sensor.SimulationSensorMagnetronTemp2.random.uniform', return_value=-0.01)
    def test_update__magnetron_inactive__decreases_temperature(self, mock_random):
        self.sensor.magnetron.active = False
        self.sensor.cooling_fan.power_share = 0
        self.sensor.temperature = AMBIENT_TEMPERATURE_IN_CELSIUS + 10
        self.sensor.update()

        self.assertEqual(self.sensor.temperature, (AMBIENT_TEMPERATURE_IN_CELSIUS + 10) - 0.05 - 0.01)

    @patch('src.components.sensor.SimulationSensorMagnetronTemp2.random.uniform', return_value=0.01)
    def test_update__cooling_fan_active__reduces_temperature(self, mock_random):
        self.sensor.magnetron.active = True
        self.sensor.cooling_fan.power_share = 0.5
        self.sensor.update()

        self.assertEqual(self.sensor.temperature, AMBIENT_TEMPERATURE_IN_CELSIUS + 0.3 - 0.4 * 0.5 + 0.01)

    @patch('src.components.sensor.SimulationSensorMagnetronTemp2.random.uniform', return_value=0.0)
    def test_update__temperature_below_ambient__clamps_to_ambient(self, mock_random):
        self.sensor.temperature = AMBIENT_TEMPERATURE_IN_CELSIUS - 10
        self.sensor.magnetron.active = False
        self.sensor.cooling_fan.power_share = 0
        self.sensor.update()

        self.assertEqual(self.sensor.temperature, AMBIENT_TEMPERATURE_IN_CELSIUS)

    def test_reset__after_update__resets_to_ambient_temperature(self):
        self.sensor.temperature = AMBIENT_TEMPERATURE_IN_CELSIUS + 10
        self.sensor.reset()

        self.assertEqual(self.sensor.temperature, AMBIENT_TEMPERATURE_IN_CELSIUS)
