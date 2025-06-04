import unittest

from src.components.cooling.MockCoolingFan import MockCoolingFan


class TestMockCoolingFan(unittest.TestCase):
    def test___init____default_power_share__equals_half(self):
        fan = MockCoolingFan()
        self.assertEqual(fan.power_share, 0.5)
