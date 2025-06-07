import unittest

from src.components.cooling.CoolingFan import CoolingFan


class TestCoolingFan(unittest.TestCase):
    def setUp(self):
        CoolingFan._instance = None
        self.cooling_fan = CoolingFan()

    def test_instance__singleton_behavior__same_instance(self):
        instance1 = CoolingFan()
        instance2 = CoolingFan()

        self.assertIs(instance1, instance2)

    def test_power_share__default_value__is_zero(self):
        self.assertEqual(self.cooling_fan.power_share, 0.0)

    def test_power_share__set_valid_value__updates_correctly(self):
        self.cooling_fan.power_share = 0.5

        self.assertEqual(self.cooling_fan.power_share, 0.5)
