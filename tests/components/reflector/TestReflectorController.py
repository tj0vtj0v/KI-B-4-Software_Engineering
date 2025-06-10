import unittest
from unittest.mock import MagicMock

from src.components.reflector.Reflector import Reflector
from src.components.reflector.ReflectorController import ReflectorController
from src.helper.config import REFLECTOR_MAX_ANGLE_IN_DEGREES, REFLECTOR_MIN_ANGLE_IN_DEGREES, REFLECTOR_STEP_IN_DEGREES
from src.helper.logging.LogLevel import LogLevel


class TestReflectorController(unittest.TestCase):
    def setUp(self):
        ReflectorController._instance = None
        self.reflector_controller = ReflectorController()
        self.reflector_controller.reflector = Reflector()
        self.reflector_controller.sensors = MagicMock()
        self.reflector_controller.logger = MagicMock()

    def test_instance__singleton_behavior__same_instance(self):
        instance1 = ReflectorController()
        instance2 = ReflectorController()

        self.assertIs(instance1, instance2)

    def test_set_angle__valid_value__updates_target_angle(self):
        self.reflector_controller.set_angle(30)

        self.assertEqual(self.reflector_controller.target_angle, 30)

    def test_set_angle__below_minimum__raises_value_error(self):
        with self.assertRaises(ValueError):
            self.reflector_controller.set_angle(REFLECTOR_MIN_ANGLE_IN_DEGREES - 1)

    def test_set_angle__above_maximum__raises_value_error(self):
        with self.assertRaises(ValueError):
            self.reflector_controller.set_angle(REFLECTOR_MAX_ANGLE_IN_DEGREES + 1)

    def test_set_angle__same_as_current_target__does_not_update(self):
        self.reflector_controller.target_angle = 30
        self.reflector_controller.set_angle(30)

        self.reflector_controller.logger.info.assert_not_called()

    def test_update__target_angle_reached__does_not_change_angle(self):
        self.reflector_controller.reflector.angle = 30
        self.reflector_controller.target_angle = 30
        self.reflector_controller.update()

        self.assertEqual(self.reflector_controller.reflector.angle, 30)

    def test_update__target_angle_lower__decreases_angle_incrementally(self):
        self.reflector_controller.reflector.angle = 40
        self.reflector_controller.target_angle = 30
        self.reflector_controller.update()

        self.assertEqual(self.reflector_controller.reflector.angle, 40 - REFLECTOR_STEP_IN_DEGREES)

    def test_update__target_angle_higher__increases_angle_incrementally(self):
        self.reflector_controller.reflector.angle = 20
        self.reflector_controller.target_angle = 30
        self.reflector_controller.update()

        self.assertEqual(self.reflector_controller.reflector.angle, 20 + REFLECTOR_STEP_IN_DEGREES)

    def test_update__angle_clamped_to_maximum__sets_to_maximum(self):
        self.reflector_controller.reflector.angle = REFLECTOR_MAX_ANGLE_IN_DEGREES + 10
        self.reflector_controller.update()

        self.assertEqual(self.reflector_controller.reflector.angle, REFLECTOR_MAX_ANGLE_IN_DEGREES)

    def test_update__angle_clamped_to_minimum__sets_to_minimum(self):
        self.reflector_controller.reflector.angle = REFLECTOR_MIN_ANGLE_IN_DEGREES - 10
        self.reflector_controller.update()

        self.assertEqual(self.reflector_controller.reflector.angle, REFLECTOR_MIN_ANGLE_IN_DEGREES)

    def test_stop__called__sets_target_angle_to_zero(self):
        self.reflector_controller.stop()

        self.assertEqual(self.reflector_controller.target_angle, 0.0)
        self.reflector_controller.logger.log.assert_called_with("Stopping reflector controller.", LogLevel.INFO)

    def test_emergency_stop__called__sets_target_angle_to_current_angle(self):
        self.reflector_controller.reflector.angle = 45
        self.reflector_controller.emergency_stop()

        self.assertEqual(self.reflector_controller.target_angle, 45)
        self.reflector_controller.logger.log.assert_called_with("Emergency stopping reflector controller.",
                                                                LogLevel.INFO)

    def test_update__target_angle_within_step__sets_to_target(self):
        self.reflector_controller.reflector.angle = 0
        self.reflector_controller.target_angle = REFLECTOR_STEP_IN_DEGREES
        self.reflector_controller.update()

        self.assertEqual(self.reflector_controller.reflector.angle, REFLECTOR_STEP_IN_DEGREES)

    def test_update__no_target_angle_set__does_not_change_angle(self):
        initial_angle = self.reflector_controller.reflector.angle
        self.reflector_controller.update()

        self.assertEqual(self.reflector_controller.reflector.angle, initial_angle)


if __name__ == "__main__":
    unittest.main()
