import unittest

from src.components.alarm.Alarm import Alarm


class TestAlarm(unittest.TestCase):
    def setUp(self):
        Alarm._instance = None
        self.alarm = Alarm()

    def test___new____singleton_behavior__returns_same_instance(self):
        alarm1 = Alarm()
        alarm2 = Alarm()

        self.assertIs(alarm1, alarm2)

    def test___init____initial_state__active_is_false(self):
        self.assertFalse(self.alarm.active)

    def test_active__modify_state__reflects_correctly(self):
        self.alarm.active = True
        self.assertTrue(self.alarm.active)

        self.alarm.active = False
        self.assertFalse(self.alarm.active)
