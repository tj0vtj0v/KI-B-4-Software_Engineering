import unittest
from unittest.mock import patch

from src.helper.Logger import Logger
from src.helper.logging.LogLevel import LogLevel


class TestLogger(unittest.TestCase):
    def test___new__with_same_service_name__returns_same_instance(self):
        logger1 = Logger("ServiceA")
        logger2 = Logger("ServiceA")
        logger3 = Logger("ServiceB")

        self.assertIs(logger1, logger2)
        self.assertIsNot(logger1, logger3)

    @patch("logging.Logger.log")
    def test_log_and_set_level__called_with_message_and_level__logs_correctly_and_sets_level(self, mock_log):
        logger = Logger("ServiceC")

        logger.log("Hello", LogLevel.INFO)
        mock_log.assert_called_with(LogLevel.INFO, "ServiceC -> Hello")

        logger.set_level(LogLevel.ERROR)
        self.assertEqual(logger._logger.level, LogLevel.ERROR)
