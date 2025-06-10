import unittest
from unittest.mock import patch

from src.components.sensor.SimulationSensorTemp2 import SimulationSensorTemp2
from src.helper.config import AMBIENT_TEMPERATURE_IN_CELSIUS


class TestSimulationSensorTemp2(unittest.TestCase):
    def setUp(self):
        SimulationSensorTemp2._instance = None
        self.sensor = SimulationSensorTemp2()

    def test_singleton__multiple_instances__same_object(self):
        sensor1 = SimulationSensorTemp2()
        sensor2 = SimulationSensorTemp2()

        self.assertIs(sensor1, sensor2)

    def test_get__default_temperature__returns_ambient_temperature(self):
        result = self.sensor.get()

        self.assertEqual(result, AMBIENT_TEMPERATURE_IN_CELSIUS)

    @patch("src.components.sensor.SimulationSensorTemp2.random.uniform", return_value=0)
    def test_update__magnetron_active__increases_temperature(self, mock_random):
        self.sensor.magnetron.active = True
        initial_temperature = self.sensor.get()
        self.sensor.update()

        self.assertGreater(self.sensor.get(), initial_temperature)

    @patch("src.components.sensor.SimulationSensorTemp2.random.uniform", return_value=0)
    def test_update__door_opened__decreases_temperature(self, mock_random):
        self.sensor.door.opened = True
        self.sensor.temperature = 50
        initial_temperature = self.sensor.get()
        self.sensor.update()

        self.assertLess(self.sensor.get(), initial_temperature)

    @patch("src.components.sensor.SimulationSensorTemp2.random.uniform", return_value=0)
    def test_update__temperature_never_below_ambient__stays_at_ambient(self, mock_random):
        self.sensor.temperature = AMBIENT_TEMPERATURE_IN_CELSIUS - 1
        self.sensor.update()

        self.assertAlmostEqual(self.sensor.get(), AMBIENT_TEMPERATURE_IN_CELSIUS, delta=0.01)

    def test_reset__after_update__resets_to_ambient_temperature(self):
        self.sensor.temperature = AMBIENT_TEMPERATURE_IN_CELSIUS + 10
        self.sensor.reset()

        self.assertEqual(self.sensor.get(), AMBIENT_TEMPERATURE_IN_CELSIUS)

    @patch("src.components.sensor.SimulationSensorTemp2.random.uniform", return_value=0)
    def test_update__door_closed_and_magnetron_inactive__temperature_decreasing(self, mock_random):
        self.sensor.door.opened = False
        self.sensor.magnetron.active = False
        self.sensor.temperature = 50
        initial_temperature = self.sensor.get()
        self.sensor.update()

        self.assertLess(self.sensor.get(), initial_temperature)

    @patch("src.components.sensor.SimulationSensorTemp2.random.uniform", return_value=0.005)
    def test_update__random_fluctuation__temperature_adjusted(self, mock_random):
        initial_temperature = self.sensor.get()
        self.sensor.update()

        self.assertAlmostEqual(self.sensor.get(), initial_temperature + 0.005, delta=0.01)

    def test_reset__invalid_temperature__resets_to_ambient_temperature(self):
        self.sensor.temperature = -100
        self.sensor.reset()

        self.assertEqual(self.sensor.get(), AMBIENT_TEMPERATURE_IN_CELSIUS)

    @patch("src.components.sensor.SimulationSensorTemp2.random.uniform", return_value=0.0)
    def test_update__invalid_temperature__clamped_to_ambient(self, mock_random):
        self.sensor.temperature = -100
        self.sensor.update()

        self.assertGreaterEqual(self.sensor.get(), AMBIENT_TEMPERATURE_IN_CELSIUS)
