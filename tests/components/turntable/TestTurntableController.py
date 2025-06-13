import unittest
from unittest.mock import MagicMock

from src.components.turntable.TurntableController import TurntableController
from src.helper.config import TURNTABLE_MIN_ROTATIONS_PER_MINUTE, TURNTABLE_MAX_ROTATIONS_PER_MINUTE, \
    TURNTABLE_STEP_IN_ROTATIONS_PER_MINUTE
from src.helper.logging.LogLevel import LogLevel


class TestTurntableController(unittest.TestCase):
    def setUp(self):
        TurntableController._instance = None
        self.controller = TurntableController()
        self.controller.logger = MagicMock()
        self.controller.turntable = MagicMock()
        self.controller.turntable.rotations_per_minute = 0.0

    def test_singleton_instance__returns_same_instance(self):
        instance1 = TurntableController()
        instance2 = TurntableController()

        self.assertIs(instance1, instance2)

    def test_initial_state__target_rotations_is_zero(self):
        self.assertEqual(self.controller.target_rotations_per_minute, 0.0)

    def test_update__target_equals_current__no_change(self):
        self.controller.turntable.rotations_per_minute = 5.0
        self.controller.target_rotations_per_minute = 5.0

        self.controller.update()

        self.assertEqual(self.controller.turntable.rotations_per_minute, 5.0)

    def test_update__target_greater_than_current__increases_rotations(self):
        self.controller.turntable.rotations_per_minute = 0.0
        self.controller.target_rotations_per_minute = 5.0

        self.controller.update()

        self.assertEqual(self.controller.turntable.rotations_per_minute, TURNTABLE_STEP_IN_ROTATIONS_PER_MINUTE)

    def test_update__target_less_than_current__decreases_rotations(self):
        self.controller.turntable.rotations_per_minute = 5.0
        self.controller.target_rotations_per_minute = 0.0

        self.controller.update()

        self.assertEqual(self.controller.turntable.rotations_per_minute, 5.0 - TURNTABLE_STEP_IN_ROTATIONS_PER_MINUTE)

    def test_update__target_greater_than_current_by_step__sets_to_target(self):
        self.controller.turntable.rotations_per_minute = 0.0
        self.controller.target_rotations_per_minute = TURNTABLE_STEP_IN_ROTATIONS_PER_MINUTE

        self.controller.update()

        self.assertEqual(self.controller.turntable.rotations_per_minute, TURNTABLE_STEP_IN_ROTATIONS_PER_MINUTE)

    def test_set_speed__valid_value__updates_target_rotations(self):
        self.controller.set_speed(3.0)

        self.assertEqual(self.controller.target_rotations_per_minute, 3.0)

    def test_set_speed__below_minimum__raises_value_error(self):
        with self.assertRaises(ValueError):
            self.controller.set_speed(TURNTABLE_MIN_ROTATIONS_PER_MINUTE - 1)

    def test_set_speed__above_maximum__raises_value_error(self):
        with self.assertRaises(ValueError):
            self.controller.set_speed(TURNTABLE_MAX_ROTATIONS_PER_MINUTE + 1)

    def test_set_speed__same_as_current_target__no_change(self):
        self.controller.target_rotations_per_minute = 3.0
        self.controller.set_speed(3.0)

        self.assertEqual(self.controller.target_rotations_per_minute, 3.0)
        self.controller.logger.log.assert_not_called()

    def test_stop__called__target_rotations_is_zero(self):
        self.controller.set_speed(3.0)
        self.controller.stop()

        self.assertEqual(self.controller.target_rotations_per_minute, 0.0)

    def test_emergency_stop__called__rotations_and_target_are_zero(self):
        self.controller.turntable.rotations_per_minute = 5.0
        self.controller.target_rotations_per_minute = 5.0

        self.controller.emergency_stop()

        self.assertEqual(self.controller.turntable.rotations_per_minute, 0.0)
        self.assertEqual(self.controller.target_rotations_per_minute, 0.0)

    def test_update__logs_debug_message(self):
        self.controller.update()

        self.controller.logger.log.assert_called_with("Updating Turntable", LogLevel.DEBUG)

    def test_set_speed__logs_info_message(self):
        self.controller.set_speed(3.0)

        self.controller.logger.log.assert_called_with("Changing the target_speed to 3.0.", LogLevel.INFO)

    def test_stop__logs_info_message(self):
        self.controller.stop()

        self.controller.logger.log.assert_called_with("Stopping turntable.", LogLevel.INFO)

    def test_emergency_stop__logs_info_message(self):
        self.controller.emergency_stop()

        self.controller.logger.log.assert_called_with("Emergency stopping turntable controller.", LogLevel.INFO)
