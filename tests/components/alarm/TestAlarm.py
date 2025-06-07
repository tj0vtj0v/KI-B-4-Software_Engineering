import unittest

from src.components.alarm.Alarm import Alarm


class TestAlarm(unittest.TestCase):
    def setUp(self):
        self.alarm = Alarm()

    def test_init__initial_state__active_is_false(self):
        self.assertFalse(self.alarm.active)
