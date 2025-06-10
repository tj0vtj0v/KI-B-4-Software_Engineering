import unittest
from unittest.mock import MagicMock, patch

from src.components.magnetron.MagnetronModulator import MagnetronModulator
from src.helper.config import MAGNETRON_MAX_POWER_SHARE_PER_MINUTE, MAGNETRON_MAX_TEMP_IN_CELSIUS
from src.helper.logging.LogLevel import LogLevel


class TestMagnetronModulator(unittest.TestCase):
    def setUp(self):
        MagnetronModulator._instance = None
        self.modulator = MagnetronModulator()
        self.modulator.logger.log = MagicMock()
        self.modulator.magnetron.turn_on = MagicMock()
        self.modulator.magnetron.turn_off = MagicMock()
        self.modulator.power_history.add = MagicMock()
        self.modulator.power_history.power_share = MagicMock(return_value=0)
        self.modulator.sensor_manager.magnetron_temp1 = MagicMock(return_value=25)
        self.modulator.sensor_manager.magnetron_temp2 = MagicMock(return_value=25)

    def test_set_target_power_share__valid_value__sets_correctly(self):
        self.modulator.target_power_share = 0.1

        for value in [0, 0.5, 1]:
            self.modulator.logger.log.reset_mock()

            self.modulator.set_target_power_share(value)

            self.assertEqual(self.modulator.target_power_share, value)
            self.modulator.logger.log.assert_called_with(f"Target power set to {value}%", LogLevel.INFO)

    def test_set_target_power_share__invalid_value__raises_value_error(self):
        for value in [-0.1, 1.1, -100, 100]:
            with self.assertRaises(ValueError):
                self.modulator.set_target_power_share(value)

    @patch("src.components.magnetron.MagnetronModulator.random.uniform", return_value=0.6)
    def test_magnetron_cycle__within_power_limit__turns_on_magnetron(self, mock_random):
        self.modulator.set_target_power_share(0.7)
        self.modulator.power_history.power_share.return_value = MAGNETRON_MAX_POWER_SHARE_PER_MINUTE - 1
        self.modulator.magnetron_cycle()

        self.modulator.magnetron.turn_on.assert_called_once()
        self.modulator.power_history.add.assert_called_with(True)

    @patch("src.components.magnetron.MagnetronModulator.random.uniform", return_value=0.8)
    def test_magnetron_cycle__random_above_target__turns_off_magnetron(self, mock_random):
        self.modulator.set_target_power_share(0.7)
        self.modulator.power_history.power_share.return_value = 0
        self.modulator.magnetron_cycle()

        self.modulator.magnetron.turn_off.assert_called_once()
        self.modulator.power_history.add.assert_called_with(False)

    @patch("src.components.magnetron.MagnetronModulator.random.uniform", return_value=0.6)
    def test_magnetron_cycle__exceeds_power_limit__skips_magnetron_cycle(self, mock_random):
        self.modulator.set_target_power_share(0.7)
        self.modulator.power_history.power_share.return_value = MAGNETRON_MAX_POWER_SHARE_PER_MINUTE + 1
        self.modulator.magnetron_cycle()

        self.modulator.magnetron.turn_on.assert_not_called()
        self.modulator.magnetron.turn_off.assert_called_once()
        self.modulator.logger.log.assert_called_with("Power share limit exceeded, skipping magnetron cycle",
                                                     LogLevel.WARNING)

    @patch("src.components.magnetron.MagnetronModulator.random.uniform", return_value=0.6)
    def test_magnetron_cycle__exceeds_temp_limit__skips_magnetron_cycle(self, mock_random):
        self.modulator.set_target_power_share(0.7)
        self.modulator.sensor_manager.magnetron_temp1.return_value = MAGNETRON_MAX_TEMP_IN_CELSIUS + 1
        self.modulator.magnetron_cycle()

        self.modulator.magnetron.turn_on.assert_not_called()
        self.modulator.magnetron.turn_off.assert_called_once()
        self.modulator.logger.log.assert_called_with(
            f"Magnetron temperature {MAGNETRON_MAX_TEMP_IN_CELSIUS + 1} exceeds limit, skipping cycle",
            LogLevel.WARNING
        )

    def test_safety_hazard__power_share_exceeded__returns_true(self):
        self.modulator.power_history.power_share.return_value = MAGNETRON_MAX_POWER_SHARE_PER_MINUTE + 1
        result = self.modulator.safety_hazard()

        self.assertTrue(result)
        self.modulator.logger.log.assert_called_with("Power share limit exceeded, skipping magnetron cycle",
                                                     LogLevel.WARNING)

    def test_safety_hazard__temperature_exceeded__returns_true(self):
        self.modulator.sensor_manager.magnetron_temp1.return_value = MAGNETRON_MAX_TEMP_IN_CELSIUS + 1
        result = self.modulator.safety_hazard()

        self.assertTrue(result)
        self.modulator.logger.log.assert_called_with(
            f"Magnetron temperature {MAGNETRON_MAX_TEMP_IN_CELSIUS + 1} exceeds limit, skipping cycle",
            LogLevel.WARNING
        )

    def test_safety_hazard__no_hazards__returns_false(self):
        self.modulator.power_history.power_share.return_value = MAGNETRON_MAX_POWER_SHARE_PER_MINUTE - 1
        self.modulator.sensor_manager.magnetron_temp1.return_value = MAGNETRON_MAX_TEMP_IN_CELSIUS - 1
        self.modulator.sensor_manager.magnetron_temp2.return_value = MAGNETRON_MAX_TEMP_IN_CELSIUS - 2

        hazard = self.modulator.safety_hazard()

        self.assertFalse(hazard)

    def test_start__modulator_running_state__is_true_and_thread_started(self):
        with patch("threading.Thread.start") as mock_start:
            self.modulator.start()

            self.assertTrue(self.modulator.running)
            self.assertIsNotNone(self.modulator.thread)
            mock_start.assert_called_once()

    def test_stop__modulator_running_state__is_false_and_thread_joined(self):
        with patch("threading.Thread.start"), patch("threading.Thread.join") as mock_join:
            self.modulator.start()
            self.modulator.stop()

            self.assertFalse(self.modulator.running)
            mock_join.assert_called_once()

    def test_stop__thread_not_initialized__does_not_throw_error(self):
        self.modulator.running = False
        self.modulator.thread = None
        self.modulator.stop()

        self.assertFalse(self.modulator.running)

    @patch("src.components.magnetron.MagnetronModulator.time.sleep", return_value=None)
    @patch.object(MagnetronModulator, "magnetron_cycle")
    def test_magnetron_loop__runs_until_running_false(self, mock_cycle, mock_sleep):
        call_count = [0]

        def stop_after_n_calls(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] >= 3:
                self.modulator.running = False

        mock_cycle.side_effect = stop_after_n_calls
        self.modulator.running = True
        self.modulator.magnetron_loop()

        self.assertEqual(call_count[0], 3)
        self.assertFalse(self.modulator.running)
