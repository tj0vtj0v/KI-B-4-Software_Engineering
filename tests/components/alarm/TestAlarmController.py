import unittest
from unittest.mock import MagicMock

from src.components.alarm.AlarmController import AlarmController
from src.helper.logging.LogLevel import LogLevel


class TestAlarmController(unittest.TestCase):
    def setUp(self):
        AlarmController._instance = None
        self.ctrl = AlarmController()
        self.mock_logger = MagicMock()
        self.ctrl.logger = self.mock_logger

    def test_AlarmController__singleton_instance__returns_same_instance(self):
        instance1 = AlarmController()
        instance2 = AlarmController()

        self.assertIs(instance1, instance2, "AlarmController is not a singleton.")

    def test_is_alarming__active_alarm__returns_true(self):
        self.ctrl.alarm.active = True
        self.assertTrue(self.ctrl.is_alarming())

    def test_is_alarming__inactive_alarm__returns_false(self):
        self.ctrl.alarm.active = False
        self.assertFalse(self.ctrl.is_alarming())

    def test_activate_alarm__inactive_alarm__activates_and_logs(self):
        self.ctrl.alarm.active = False
        self.ctrl.activate_alarm()

        self.assertTrue(self.ctrl.alarm.active)
        self.mock_logger.log.assert_called_with("Activating alarm.", level=LogLevel.INFO)

    def test_activate_alarm__already_active__logs_warning(self):
        self.ctrl.alarm.active = True
        self.ctrl.activate_alarm()

        self.assertTrue(self.ctrl.alarm.active)
        self.mock_logger.log.assert_called_with("Alarm is already active.", level=LogLevel.WARNING)

    def test_deactivate_alarm__active_alarm__deactivates_and_logs(self):
        self.ctrl.alarm.active = True
        self.ctrl.deactivate_alarm()

        self.assertFalse(self.ctrl.alarm.active)
        self.mock_logger.log.assert_called_with("Deactivating alarm.", level=LogLevel.INFO)

    def test_deactivate_alarm__already_inactive__logs_warning(self):
        self.ctrl.alarm.active = False
        self.ctrl.deactivate_alarm()

        self.assertFalse(self.ctrl.alarm.active)
        self.mock_logger.log.assert_called_with("Alarm is already inactive.", level=LogLevel.WARNING)
