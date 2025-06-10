import unittest

from src.components.turntable.Turntable import Turntable


class TestTurntable(unittest.TestCase):
    def setUp(self):
        Turntable._instance = None
        self.turntable = Turntable()

    def test___new____singleton_instance__returns_same_instance(self):
        instance1 = Turntable()
        instance2 = Turntable()

        self.assertIs(instance1, instance2)

    def test___init____initial_state__rotations_per_minute_is_zero(self):
        self.assertEqual(self.turntable.rotations_per_minute, 0.0)

    def test_set_rotations_per_minute__valid_value__updates_rotations(self):
        self.turntable.rotations_per_minute = 10.0

        self.assertEqual(self.turntable.rotations_per_minute, 10.0)

    def test_set_rotations_per_minute__negative_value__updates_rotations(self):
        self.turntable.rotations_per_minute = -5.0

        self.assertEqual(self.turntable.rotations_per_minute, -5.0)

    def test_stop__called__rotations_per_minute_is_zero(self):
        self.turntable.rotations_per_minute = 15.0
        self.turntable.rotations_per_minute = 0.0

        self.assertEqual(self.turntable.rotations_per_minute, 0.0)
