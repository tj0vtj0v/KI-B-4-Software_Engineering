import unittest
from unittest.mock import MagicMock

from src.components.cooling.CoolingFan import CoolingFan
from src.components.cooling.CoolingFanController import CoolingFanController
from src.helper.config import AMBIENT_TEMPERATURE_IN_CELSIUS


class TestCoolingFanController(unittest.TestCase):
    def setUp(self):
        CoolingFanController._instance = None
        self.cooling_fan_controller = CoolingFanController()
        self.cooling_fan_controller.cooling_fan = CoolingFan()
        self.cooling_fan_controller.sensors = MagicMock()
        self.cooling_fan_controller.sensors.magnetron_temp1.return_value = AMBIENT_TEMPERATURE_IN_CELSIUS
        self.cooling_fan_controller.sensors.magnetron_temp2.return_value = AMBIENT_TEMPERATURE_IN_CELSIUS

    def test_instance__singleton_behavior__same_instance(self):
        instance1 = CoolingFanController()
        instance2 = CoolingFanController()

        self.assertIs(instance1, instance2)

    def test_set_target_power_share__valid_value__updates_correctly(self):
        self.cooling_fan_controller.set_target_power_share(0.5)

        self.assertEqual(self.cooling_fan_controller.target_power_share, 0.5)

    def test_update__sensor_values__updates_power_share(self):
        self.cooling_fan_controller.sensors.magnetron_temp1.return_value = 80.0
        self.cooling_fan_controller.sensors.magnetron_temp2.return_value = 100.0
        self.cooling_fan_controller.update()

        self.assertGreater(self.cooling_fan_controller.cooling_fan.power_share, 0.0)

    def test_update__target_power_share_lower__adjusts_incrementally(self):
        self.cooling_fan_controller.cooling_fan.power_share = 0.2
        self.cooling_fan_controller.set_target_power_share(0.5)
        self.cooling_fan_controller.update()

        self.assertGreater(self.cooling_fan_controller.cooling_fan.power_share, 0.2)

    def test_update__target_power_share_higher__adjusts_incrementally(self):
        self.cooling_fan_controller.cooling_fan.power_share = 0.8
        self.cooling_fan_controller.set_target_power_share(0.5)
        self.cooling_fan_controller.update()

        self.assertLess(self.cooling_fan_controller.cooling_fan.power_share, 0.8)

    def test_start__sets_initial_power_share(self):
        self.cooling_fan_controller.start()

        self.assertEqual(self.cooling_fan_controller.target_power_share, 0.2)

    def test_stop__sets_power_share_to_zero(self):
        self.cooling_fan_controller.stop()

        self.assertEqual(self.cooling_fan_controller.target_power_share, 0.0)

    def test_update__power_share_clamped_to_maximum(self):
        self.cooling_fan_controller.cooling_fan.power_share = 1.1
        self.cooling_fan_controller.update()

        self.assertLessEqual(self.cooling_fan_controller.cooling_fan.power_share, 1.0)

    def test_update__power_share_clamped_to_minimum(self):
        self.cooling_fan_controller.cooling_fan.power_share = -0.1
        self.cooling_fan_controller.update()

        self.assertGreaterEqual(self.cooling_fan_controller.cooling_fan.power_share, 0.0)

    def test_magnetron_temp_to_power_share__below_absolute_zero__returns_zero(self):
        self.assertEqual(self.cooling_fan_controller.magnetron_temp_to_power_share(-300.0), 0.0)

    def test_magnetron_temp_to_power_share__exactly_zero__returns_zero(self):
        self.assertEqual(self.cooling_fan_controller.magnetron_temp_to_power_share(0.0), 0.0)

    def test_magnetron_temp_to_power_share__at_50__returns_zero(self):
        self.assertEqual(self.cooling_fan_controller.magnetron_temp_to_power_share(50.0), 0.0)

    def test_magnetron_temp_to_power_share__between_50_and_100__returns_scaled_value(self):
        self.assertAlmostEqual(self.cooling_fan_controller.magnetron_temp_to_power_share(75.0), 0.125)

    def test_magnetron_temp_to_power_share__at_100__returns_0_point_25(self):
        self.assertAlmostEqual(self.cooling_fan_controller.magnetron_temp_to_power_share(100.0), 0.25)

    def test_magnetron_temp_to_power_share__between_100_and_150__returns_scaled_value(self):
        self.assertAlmostEqual(self.cooling_fan_controller.magnetron_temp_to_power_share(125.0), 0.625)

    def test_magnetron_temp_to_power_share__just_below_150__returns_below_one(self):
        self.assertAlmostEqual(self.cooling_fan_controller.magnetron_temp_to_power_share(149.9), 0.9985, places=4)

    def test_magnetron_temp_to_power_share__at_150__returns_one(self):
        self.assertEqual(self.cooling_fan_controller.magnetron_temp_to_power_share(150.0), 1.0)

    def test_magnetron_temp_to_power_share__well_above_150__returns_one(self):
        self.assertEqual(self.cooling_fan_controller.magnetron_temp_to_power_share(200.0), 1.0)
