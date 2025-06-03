import unittest
from unittest.mock import patch

from src.components.sensor.SimulationSensorMagnetronTemp1 import SimulationSensorMagnetronTemp1
from src.helper.config import AMBIENT_TEMPERATURE_IN_CELSIUS


class TestSimulationSensorMagnetronTemp1(unittest.TestCase):
    def setUp(self):
        SimulationSensorMagnetronTemp1._instance = None
        self.sensor = SimulationSensorMagnetronTemp1()

    def test_singleton__multiple_instances__same_object(self):
        sensor1 = SimulationSensorMagnetronTemp1()
        sensor2 = SimulationSensorMagnetronTemp1()
        self.assertIs(sensor1, sensor2)

    def test_get__initial_state__returns_ambient_temperature(self):
        self.assertEqual(self.sensor.get(), AMBIENT_TEMPERATURE_IN_CELSIUS)

    def test_update__magnetron_active__increases_temperature(self):
        self.sensor.magnetron.active = True
        initial_temperature = self.sensor.get()
        self.sensor.update()

        self.assertGreater(self.sensor.get(), initial_temperature)

    def test_update__magnetron_inactive__decreases_temperature(self):
        self.sensor.magnetron.active = False
        self.sensor.temperature = AMBIENT_TEMPERATURE_IN_CELSIUS + 10
        initial_temperature = self.sensor.get()
        self.sensor.update()

        self.assertLess(self.sensor.get(), initial_temperature)

    def test_update__cooling_fan_active__reduces_temperature_increase(self):
        self.sensor.magnetron.active = True
        self.sensor.cooling_fan.power_share = 0.5
        initial_temperature = self.sensor.get()
        self.sensor.update()

        self.assertGreater(self.sensor.get(), initial_temperature)
        self.assertLess(self.sensor.get(), initial_temperature + 0.3)

    def test_update__temperature_below_ambient__resets_to_ambient(self):
        self.sensor.temperature = AMBIENT_TEMPERATURE_IN_CELSIUS - 5
        self.sensor.update()

        self.assertAlmostEqual(self.sensor.get(), AMBIENT_TEMPERATURE_IN_CELSIUS, delta=0.01)

    def test_reset__after_updates__resets_to_ambient_temperature(self):
        self.sensor.temperature = AMBIENT_TEMPERATURE_IN_CELSIUS + 10
        self.sensor.reset()

        self.assertEqual(self.sensor.get(), AMBIENT_TEMPERATURE_IN_CELSIUS)

    def test_update__cooling_fan_inactive__temperature_increases_normally(self):
        self.sensor.magnetron.active = True
        self.sensor.cooling_fan.power_share = 0.0
        initial_temperature = self.sensor.get()
        self.sensor.update()

        self.assertAlmostEqual(self.sensor.get(), initial_temperature + 0.3, delta=0.01)

    def test_update__cooling_fan_full_power__temperature_decreases(self):
        self.sensor.magnetron.active = True
        self.sensor.cooling_fan.power_share = 1.0
        self.sensor.temperature = AMBIENT_TEMPERATURE_IN_CELSIUS + 10
        initial_temperature = self.sensor.get()
        self.sensor.update()

        self.assertLess(self.sensor.get(), initial_temperature)

    def test_update__random_fluctuation_negative__temperature_varies_within_bounds(self):
        with patch("random.uniform", return_value=-0.01):
            initial_temperature = self.sensor.get()
            self.sensor.update()

            self.assertAlmostEqual(self.sensor.get(), initial_temperature - 0.01, delta=0.01)
