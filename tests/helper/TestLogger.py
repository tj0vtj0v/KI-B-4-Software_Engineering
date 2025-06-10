import unittest
from unittest.mock import patch

from src.helper.Logger import Logger
from src.helper.config import DEFAULT_LOG_LEVEL
from src.helper.logging.LogLevel import LogLevel


class TestLogger(unittest.TestCase):
    def setUp(self):
        Logger._instances = {}
        self.service_name = "TestService"
        self.default_level = DEFAULT_LOG_LEVEL

    def test___new__with_same_service_name__returns_same_instance(self):
        logger1 = Logger("ServiceA")
        logger2 = Logger("ServiceA")
        logger3 = Logger("ServiceB")

        self.assertIs(logger1, logger2)
        self.assertIsNot(logger1, logger3)

    def test___new__with_default_level__uses_default_log_level(self):
        logger = Logger(self.service_name)

        self.assertEqual(logger._logger.level, LogLevel(self.default_level))

    def test___new__with_custom_level__uses_custom_log_level(self):
        custom_level = LogLevel.ERROR
        logger = Logger(self.service_name, custom_level)

        self.assertEqual(logger._logger.level, custom_level)

    @patch("logging.Logger.log")
    def test_log__valid_message_and_level__logs_correctly(self, mock_log):
        logger = Logger(self.service_name)
        message = "Test message"
        level = LogLevel.INFO
        logger.log(message, level)

        mock_log.assert_called_once_with(level, f"{self.service_name} -> {message}")

    @patch("logging.Logger.log")
    def test_log__empty_message__does_not_log(self, mock_log):
        logger = Logger(self.service_name)
        logger.log("", LogLevel.INFO)

        mock_log.assert_not_called()
