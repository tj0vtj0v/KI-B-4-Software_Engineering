import unittest

from src.components.sensor.SimulationSensorTemp1 import SimulationSensorTemp1
from src.helper.config import AMBIENT_TEMPERATURE_IN_CELSIUS


class TestSimulationSensorTemp1(unittest.TestCase):
    def setUp(self):
        SimulationSensorTemp1._instance = None
        self.sensor = SimulationSensorTemp1()

    def test_singleton__multiple_instances__same_object(self):
        sensor1 = SimulationSensorTemp1()
        sensor2 = SimulationSensorTemp1()

        self.assertIs(sensor1, sensor2)

    def test_get__default_temperature__returns_ambient_temperature(self):
        self.assertEqual(self.sensor.get(), AMBIENT_TEMPERATURE_IN_CELSIUS)

    def test_update__magnetron_active__increases_temperature(self):
        self.sensor.magnetron.active = True
        initial_temperature = self.sensor.get()
        self.sensor.update()

        self.assertGreater(self.sensor.get(), initial_temperature)

    def test_update__door_opened__decreases_temperature(self):
        self.sensor.door.opened = True
        self.sensor.temperature = 50
        initial_temperature = self.sensor.get()
        self.sensor.update()

        self.assertLess(self.sensor.get(), initial_temperature)

    def test_update__temperature_never_below_ambient__stays_at_ambient(self):
        self.sensor.temperature = AMBIENT_TEMPERATURE_IN_CELSIUS - 1
        self.sensor.update()

        self.assertAlmostEqual(self.sensor.get(), AMBIENT_TEMPERATURE_IN_CELSIUS, delta=0.01)

    def test_reset__after_update__resets_to_ambient_temperature(self):
        self.sensor.temperature = AMBIENT_TEMPERATURE_IN_CELSIUS + 10
        self.sensor.reset()

        self.assertEqual(self.sensor.get(), AMBIENT_TEMPERATURE_IN_CELSIUS)

    def test_update__door_closed_and_magnetron_inactive__temperature_decreasing(self):
        self.sensor.door.opened = False
        self.sensor.magnetron.active = False
        self.sensor.temperature = 50
        initial_temperature = self.sensor.get()
        self.sensor.update()

        self.assertLess(self.sensor.get(), initial_temperature)
