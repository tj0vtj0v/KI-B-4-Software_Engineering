import unittest
from unittest.mock import MagicMock, patch

from src.components.cooling.CoolingFanController import CoolingFanController
from src.helper.config import COOLING_FAN_STEP_IN_PERCENT, AMBIENT_TEMPERATURE_IN_CELSIUS
from src.helper.logging.LogLevel import LogLevel


class TestCoolingFanController(unittest.TestCase):
    def setUp(self):
        CoolingFanController._instance = None
        self.cooling_fan_controller = CoolingFanController()
        self.cooling_fan_controller.cooling_fan = MagicMock()
        self.cooling_fan_controller.sensors = MagicMock()
        self.cooling_fan_controller.logger = MagicMock()
        self.cooling_fan_controller.sensors.magnetron_temp1.return_value = AMBIENT_TEMPERATURE_IN_CELSIUS
        self.cooling_fan_controller.sensors.magnetron_temp2.return_value = AMBIENT_TEMPERATURE_IN_CELSIUS

    def test_instance__singleton_behavior__same_instance(self):
        instance1 = CoolingFanController()
        instance2 = CoolingFanController()

        self.assertIs(instance1, instance2)

    def test_start__not_running__starts_thread(self):
        with patch("threading.Thread.start") as mock_start:
            self.cooling_fan_controller.start()

            self.assertTrue(self.cooling_fan_controller.running)
            mock_start.assert_called_once()

    def test_start__already_running__logs_warning(self):
        self.cooling_fan_controller.running = True
        self.cooling_fan_controller.start()

        self.cooling_fan_controller.logger.log.assert_called_with("Cooling Fan is already running", LogLevel.WARNING)

    def test_stop__running__sets_cooldown(self):
        self.cooling_fan_controller.running = True
        self.cooling_fan_controller.stop()

        self.assertTrue(self.cooling_fan_controller.cooldown)

    def test_stop__not_running__logs_warning(self):
        self.cooling_fan_controller.running = False
        self.cooling_fan_controller.stop()

        self.cooling_fan_controller.logger.log.assert_called_with("Cooling Fan is already stopped", LogLevel.WARNING)

    def test_emergency_stop__running__stops_thread(self):
        self.cooling_fan_controller.running = True
        self.cooling_fan_controller.thread = MagicMock()
        self.cooling_fan_controller.emergency_stop()

        self.assertTrue(self.cooling_fan_controller.emergency)
        self.cooling_fan_controller.thread.join.assert_called_once()

    def test_emergency_stop__not_running__logs_warning(self):
        self.cooling_fan_controller.running = False
        self.cooling_fan_controller.emergency_stop()

        self.cooling_fan_controller.logger.log.assert_called_with("Cooling Fan is already stopped", LogLevel.WARNING)

    def test_cooling_fan_cycle__updates_target_power_share(self):
        self.cooling_fan_controller.sensors.magnetron_temp1.return_value = 80.0
        self.cooling_fan_controller.sensors.magnetron_temp2.return_value = 100.0
        self.cooling_fan_controller.cooling_fan.power_share = 0.0
        self.cooling_fan_controller.target_power_share = 0.0
        self.cooling_fan_controller.cooling_fan_cycle()

        self.assertGreater(self.cooling_fan_controller.target_power_share, 0.0)

    def test_cooling_fan_cycle__cooldown_and_low_power__stops_running(self):
        self.cooling_fan_controller.cooldown = True
        self.cooling_fan_controller.target_power_share = COOLING_FAN_STEP_IN_PERCENT
        self.cooling_fan_controller.cooling_fan_cycle()

        self.assertFalse(self.cooling_fan_controller.running)

    def test_cooling_fan_cycle__clamps_power_share_to_maximum(self):
        self.cooling_fan_controller.cooling_fan.power_share = 1.1
        self.cooling_fan_controller.cooling_fan_cycle()

        self.assertLessEqual(self.cooling_fan_controller.cooling_fan.power_share, 1.0)

    def test_cooling_fan_cycle__clamps_power_share_to_minimum(self):
        self.cooling_fan_controller.cooling_fan.power_share = -0.1
        self.cooling_fan_controller.cooling_fan_cycle()

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
