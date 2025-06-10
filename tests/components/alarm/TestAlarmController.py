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
        self.ctrl.alarm = MagicMock()

    def test_AlarmController__singleton_instance__returns_same_instance(self):
        instance1 = AlarmController()
        instance2 = AlarmController()

        self.assertIs(instance1, instance2)

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
        self.mock_logger.log.assert_called_with("Activating alarm.", LogLevel.INFO)

    def test_activate_alarm__already_active__logs_warning(self):
        self.ctrl.alarm.active = True
        self.ctrl.activate_alarm()

        self.assertTrue(self.ctrl.alarm.active)
        self.mock_logger.log.assert_called_with("Alarm is already active.", LogLevel.WARNING)

    def test_deactivate_alarm__active_alarm__deactivates_and_logs(self):
        self.ctrl.alarm.active = True
        self.ctrl.deactivate_alarm()

        self.assertFalse(self.ctrl.alarm.active)
        self.mock_logger.log.assert_called_with("Deactivating alarm.", LogLevel.INFO)

    def test_deactivate_alarm__already_inactive__logs_warning(self):
        self.ctrl.alarm.active = False
        self.ctrl.deactivate_alarm()

        self.assertFalse(self.ctrl.alarm.active)
        self.mock_logger.log.assert_called_with("Alarm is already inactive.", LogLevel.WARNING)

    def test_activate_alarm__logger_failure__raises_exception(self):
        self.ctrl.alarm.active = False
        self.mock_logger.log.side_effect = Exception("Logger failure")

        with self.assertRaises(Exception) as context:
            self.ctrl.activate_alarm()
        self.assertEqual(str(context.exception), "Logger failure")

    def test_deactivate_alarm__logger_failure__raises_exception(self):
        self.ctrl.alarm.active = True
        self.mock_logger.log.side_effect = Exception("Logger failure")

        with self.assertRaises(Exception) as context:
            self.ctrl.deactivate_alarm()
        self.assertEqual(str(context.exception), "Logger failure")
