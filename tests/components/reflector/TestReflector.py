import unittest

from src.components.reflector.Reflector import Reflector


class TestReflector(unittest.TestCase):
    def setUp(self):
        Reflector._instance = None
        self.reflector = Reflector()

    def test_reflector_initialization__new_instance__angle_is_zero(self):
        self.assertEqual(self.reflector.angle, 0)

    def test_singleton__multiple_instances__same_instance(self):
        instance1 = Reflector()
        instance2 = Reflector()

        self.assertIs(instance1, instance2)

    def test_angle__set_valid_value__updates_angle(self):
        self.reflector.angle = 45

        self.assertEqual(self.reflector.angle, 45)
