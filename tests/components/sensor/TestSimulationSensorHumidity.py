import unittest
from unittest.mock import patch

from src.components.sensor.SimulationSensorHumidity import SimulationSensorHumidity
from src.helper.config import AMBIENT_HUMIDITY_IN_PERCENT


class TestSimulationSensorHumidity(unittest.TestCase):
    def setUp(self):
        SimulationSensorHumidity._instance = None
        self.sensor = SimulationSensorHumidity()

    def test_singleton__multiple_instances__same_object(self):
        sensor1 = SimulationSensorHumidity()
        sensor2 = SimulationSensorHumidity()

        self.assertIs(sensor1, sensor2)

    def test_get__default_humidity__returns_ambient_humidity(self):
        result = self.sensor.get()

        self.assertEqual(result, AMBIENT_HUMIDITY_IN_PERCENT)

    def test_update__magnetron_active__increases_humidity(self):
        self.sensor.magnetron.active = True
        initial_humidity = self.sensor.get()
        self.sensor.update()

        self.assertGreater(self.sensor.get(), initial_humidity)

    def test_update__door_opened__decreases_humidity(self):
        self.sensor.door.opened = True
        self.sensor.humidity = AMBIENT_HUMIDITY_IN_PERCENT + 10
        initial_humidity = self.sensor.get()
        self.sensor.update()

        self.assertLess(self.sensor.get(), initial_humidity)

    def test_update__humidity_never_below_ambient__stays_at_ambient(self):
        self.sensor.humidity = AMBIENT_HUMIDITY_IN_PERCENT - 1
        self.sensor.update()

        self.assertAlmostEqual(self.sensor.get(), AMBIENT_HUMIDITY_IN_PERCENT, delta=0.01)

    def test_reset__after_update__resets_to_ambient_humidity(self):
        self.sensor.humidity = AMBIENT_HUMIDITY_IN_PERCENT + 10
        self.sensor.reset()

        self.assertEqual(self.sensor.get(), AMBIENT_HUMIDITY_IN_PERCENT)

    def test_update__door_closed_and_magnetron_inactive__humidity_decreasing(self):
        self.sensor.door.opened = False
        self.sensor.magnetron.active = False
        self.sensor.humidity = AMBIENT_HUMIDITY_IN_PERCENT + 10
        initial_humidity = self.sensor.get()
        self.sensor.update()

        self.assertLess(self.sensor.get(), initial_humidity)

    @patch("src.components.sensor.SimulationSensorHumidity.random.uniform", return_value=0.01)
    def test_update__random_fluctuation__applies_fluctuation(self, mock_random):
        initial_humidity = self.sensor.get()
        self.sensor.update()

        self.assertAlmostEqual(self.sensor.get(), initial_humidity + 0.01, delta=0.01)
