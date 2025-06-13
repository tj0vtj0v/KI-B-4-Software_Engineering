import unittest
from unittest.mock import MagicMock

from src.helper.Action import Action
from src.helper.logging.LogLevel import LogLevel
from src.user.InputDetector import InputDetector


class TestInputDetector(unittest.TestCase):
    def setUp(self):
        self.input_detector = None
        self.input_detector = InputDetector()
        self.input_detector.logger = MagicMock()

    def test_start__not_delegating__logs_and_starts_listener(self):
        self.input_detector.listener.start = MagicMock()
        self.input_detector.start()

        self.input_detector.logger.log.assert_called_once_with("Starting input detection", LogLevel.INFO)
        self.assertTrue(self.input_detector.delegating)

    def test_start__already_delegating__logs_warning(self):
        self.input_detector.delegating = True
        self.input_detector.start()

        self.input_detector.logger.log.assert_called_once_with("Input detection is already running", LogLevel.WARNING)

    def test_stop__delegating__logs_and_stops_listener(self):
        self.input_detector.delegating = True
        self.input_detector.listener.stop = MagicMock()
        self.input_detector.stop()

        self.input_detector.logger.log.assert_called_once_with("Stopping input detection", LogLevel.INFO)
        self.assertFalse(self.input_detector.delegating)

    def test_stop__not_delegating__logs_warning(self):
        self.input_detector.delegating = False
        self.input_detector.stop()

        self.input_detector.logger.log.assert_called_once_with("Input detection is not running", LogLevel.WARNING)

    def test_get_latest_action__key_o__returns_open_door_action(self):
        self.input_detector.delegating = True
        self.input_detector.latest_key = MagicMock(char='o')
        action = self.input_detector.get_latest_action()

        self.assertEqual(action, Action.OPEN_DOOR)

    def test_get_latest_action__key_c__returns_close_door_action(self):
        self.input_detector.delegating = True
        self.input_detector.latest_key = MagicMock(char='c')
        action = self.input_detector.get_latest_action()

        self.assertEqual(action, Action.CLOSE_DOOR)

    def test_get_latest_action__not_delegating__returns_none(self):
        self.input_detector.delegating = False
        action = self.input_detector.get_latest_action()

        self.assertIsNone(action)

    def test_get_latest_action__no_latest_key__returns_none(self):
        self.input_detector.delegating = True
        self.input_detector.latest_key = None
        action = self.input_detector.get_latest_action()

        self.assertIsNone(action)
