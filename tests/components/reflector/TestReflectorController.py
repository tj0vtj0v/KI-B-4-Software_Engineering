import unittest
from unittest.mock import MagicMock

from src.components.reflector.Reflector import Reflector
from src.components.reflector.ReflectorController import ReflectorController
from src.helper.config import REFLECTOR_MAX_ANGLE_IN_DEGREES, REFLECTOR_MIN_ANGLE_IN_DEGREES, REFLECTOR_STEP_IN_DEGREES


class TestReflectorController(unittest.TestCase):
    def setUp(self):
        ReflectorController._instance = None
        self.reflector_controller = ReflectorController()
        self.reflector_controller.reflector = Reflector()
        self.reflector_controller.sensors = MagicMock()

    def test_instance__singleton_behavior__same_instance(self):
        instance1 = ReflectorController()
        instance2 = ReflectorController()

        self.assertIs(instance1, instance2)

    def test_set_target_angle__valid_value__updates_correctly(self):
        self.reflector_controller.set_angle(30)

        self.assertEqual(self.reflector_controller.target_angle, 30)

    def test_set_target_angle__below_minimum__raises_value_error(self):
        with self.assertRaises(ValueError):
            self.reflector_controller.set_angle(REFLECTOR_MIN_ANGLE_IN_DEGREES - 1)

    def test_set_target_angle__above_maximum__raises_value_error(self):
        with self.assertRaises(ValueError):
            self.reflector_controller.set_angle(REFLECTOR_MAX_ANGLE_IN_DEGREES + 1)

    def test_update__sensor_values__updates_angle(self):
        self.reflector_controller.set_angle(30)
        self.reflector_controller.update()

        self.assertGreater(self.reflector_controller.reflector.angle, 0)

    def test_update__target_angle_lower__adjusts_incrementally(self):
        self.reflector_controller.reflector.angle = 20
        self.reflector_controller.set_angle(40)
        self.reflector_controller.update()

        self.assertGreater(self.reflector_controller.reflector.angle, 20)

    def test_update__target_angle_higher__adjusts_incrementally(self):
        self.reflector_controller.reflector.angle = 60
        self.reflector_controller.set_angle(40)
        self.reflector_controller.update()

        self.assertLess(self.reflector_controller.reflector.angle, 60)

    def test_stop__sets_angle_to_zero(self):
        self.reflector_controller.stop()

        self.assertEqual(self.reflector_controller.target_angle, 0)

    def test_update__angle_clamped_to_maximum(self):
        self.reflector_controller.reflector.angle = REFLECTOR_MAX_ANGLE_IN_DEGREES + 10
        self.reflector_controller.update()

        self.assertEqual(self.reflector_controller.reflector.angle, REFLECTOR_MAX_ANGLE_IN_DEGREES)

    def test_update__angle_clamped_to_minimum(self):
        self.reflector_controller.reflector.angle = REFLECTOR_MIN_ANGLE_IN_DEGREES - 10
        self.reflector_controller.update()

        self.assertEqual(self.reflector_controller.reflector.angle, REFLECTOR_MIN_ANGLE_IN_DEGREES)

    def test_update__target_greater_than_current_by_step__sets_to_target(self):
        self.reflector_controller.reflector.angle = 0.0
        self.reflector_controller.target_angle = REFLECTOR_STEP_IN_DEGREES

        self.reflector_controller.update()

        self.assertEqual(self.reflector_controller.reflector.angle, REFLECTOR_STEP_IN_DEGREES)

    def test_emergency_stop__called__angle_and_target_are_zero(self):
        self.reflector_controller.reflector.angle = 45
        self.reflector_controller.target_angle = 0

        self.reflector_controller.emergency_stop()

        self.assertEqual(self.reflector_controller.reflector.angle, 45)
        self.assertEqual(self.reflector_controller.target_angle, 45)

    def test_update__no_target_angle_set__does_not_change_angle(self):
        initial_angle = self.reflector_controller.reflector.angle

        self.reflector_controller.update()

        self.assertEqual(self.reflector_controller.reflector.angle, initial_angle)


if __name__ == "__main__":
    unittest.main()
