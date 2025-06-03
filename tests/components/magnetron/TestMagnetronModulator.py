import unittest
from unittest.mock import MagicMock, patch

from src.components.magnetron.MagnetronModulator import MagnetronModulator
from src.helper.config import MAGNETRON_MAX_POWER_SHARE_PER_MINUTE, MAGNETRON_MAX_TEMP_IN_CELSIUS
from src.helper.logging.LogLevel import LogLevel


class TestMagnetronModulator(unittest.TestCase):
    def setUp(self):
        self.modulator = MagnetronModulator()
        self.modulator.logger.log = MagicMock()
        self.modulator.magnetron.turn_on = MagicMock()
        self.modulator.magnetron.turn_off = MagicMock()
        self.modulator.power_history.add = MagicMock()
        self.modulator.power_history.power_share = MagicMock(return_value=0)
        self.modulator.sensor_manager.magnetron_temp1_sensor = MagicMock(return_value=25)
        self.modulator.sensor_manager.magnetron_temp2_sensor = MagicMock(return_value=25)

    def test_set_target_power__valid_value__sets_correctly(self):
        self.modulator.set_target_power(0.5)

        self.assertEqual(self.modulator.target_power_share, 0.5)
        self.modulator.logger.log.assert_called_with("Target power set to 0.5 watts", level=LogLevel.INFO)

    def test_set_target_power__invalid_value__raises_value_error(self):
        with self.assertRaises(ValueError):
            self.modulator.set_target_power(-0.1)

        with self.assertRaises(ValueError):
            self.modulator.set_target_power(1.1)

    @patch("src.components.magnetron.MagnetronModulator.random.uniform", return_value=0.6)
    def test_magnetron_cycle__within_power_limit__turns_on_magnetron(self, mock_random):
        self.modulator.set_target_power(0.7)
        self.modulator.power_history.power_share.return_value = MAGNETRON_MAX_POWER_SHARE_PER_MINUTE - 1
        self.modulator.running = True
        self.modulator.magnetron_cycle()

        self.modulator.magnetron.turn_on.assert_called_once()
        self.modulator.power_history.add.assert_called_with(True)

    @patch("src.components.magnetron.MagnetronModulator.random.uniform", return_value=0.6)
    def test_magnetron_cycle__exceeds_power_limit__skips_magnetron_cycle(self, mock_random):
        self.modulator.set_target_power(0.7)
        self.modulator.power_history.power_share.return_value = MAGNETRON_MAX_POWER_SHARE_PER_MINUTE + 1
        self.modulator.running = True
        self.modulator.magnetron_cycle()

        self.modulator.magnetron.turn_on.assert_not_called()
        self.modulator.magnetron.turn_off.assert_called()
        self.modulator.logger.log.assert_called_with("Power share limit exceeded, skipping magnetron cycle",
                                                     level=LogLevel.WARNING)

    def test_start__modulator_running_state__is_true(self):
        with patch("threading.Thread.start"), patch("threading.Event.wait",
                                                    side_effect=lambda _: setattr(self.modulator, "running", False)):
            self.modulator.start()
            self.assertTrue(self.modulator.running)

    def test_stop__modulator_running_state__is_false(self):
        with patch("threading.Thread.start"), patch("threading.Thread.join"):
            self.modulator.start()
            self.modulator.stop()

            self.assertFalse(self.modulator.running)

    def test_magnetron_cycle__loop_execution__stops_when_running_is_false(self):
        self.modulator.running = True
        self.modulator.set_target_power(1.0)
        self.modulator.magnetron.turn_on = MagicMock()
        self.modulator.magnetron_cycle()

        self.modulator.magnetron.turn_on.assert_called_once()

    @patch("src.components.magnetron.MagnetronModulator.random.uniform", return_value=0.6)
    def test_magnetron_cycle__exceeds_temp_limit__skips_magnetron_cycle(self, mock_random):
        self.modulator.set_target_power(0.7)
        self.modulator.sensor_manager.magnetron_temp1_sensor.return_value = MAGNETRON_MAX_TEMP_IN_CELSIUS + 1
        self.modulator.running = True
        self.modulator.magnetron_cycle()

        self.modulator.magnetron.turn_on.assert_not_called()
        self.modulator.magnetron.turn_off.assert_called()
        self.modulator.logger.log.assert_called_with(
            f"Magnetron temperature {MAGNETRON_MAX_TEMP_IN_CELSIUS + 1} exceeds limit, skipping cycle",
            level=LogLevel.WARNING
        )

    def test_safety_hazard__power_share_exceeded__returns_true(self):
        self.modulator.power_history.power_share.return_value = MAGNETRON_MAX_POWER_SHARE_PER_MINUTE + 1
        result = self.modulator.safety_hazard()

        self.assertTrue(result)
        self.modulator.logger.log.assert_called_with("Power share limit exceeded, skipping magnetron cycle",
                                                     level=LogLevel.WARNING)

    def test_safety_hazard__temperature_exceeded__returns_true(self):
        self.modulator.sensor_manager.magnetron_temp1_sensor.return_value = MAGNETRON_MAX_TEMP_IN_CELSIUS + 1
        result = self.modulator.safety_hazard()

        self.assertTrue(result)
        self.modulator.logger.log.assert_called_with(
            f"Magnetron temperature {MAGNETRON_MAX_TEMP_IN_CELSIUS + 1} exceeds limit, skipping cycle",
            level=LogLevel.WARNING
        )

    def test_safety_hazard__no_hazards__returns_false(self):
        self.modulator.power_history.power_share.return_value = MAGNETRON_MAX_POWER_SHARE_PER_MINUTE - 1
        self.modulator.sensor_manager.magnetron_temp1_sensor.return_value = MAGNETRON_MAX_TEMP_IN_CELSIUS - 1
        hazard = self.modulator.safety_hazard()

        self.assertFalse(hazard)

    def test_stop__thread_not_initialized__does_not_throw_error(self):
        self.modulator.running = False
        self.modulator.thread = None
        self.modulator.stop()

        self.assertFalse(self.modulator.running)
