import unittest
from unittest.mock import patch

from src.helper.logging.LogLevel import LogLevel
from src.helper.logging.LoggerFacade import LoggerFacade


class TestLoggerFacade(unittest.TestCase):
    def setUp(self):
        self.facade = LoggerFacade(level=LogLevel.INFO, service="TestService")

    @patch("logging.Logger.log")
    def test_log__info_level__logs_info(self, mock_log):
        self.facade.log("Test message", LogLevel.INFO)
        mock_log.assert_called_with(LogLevel.INFO, "TestService -> Test message")

    @patch("logging.Logger.log")
    def test_log__debug_level__logs_debug(self, mock_log):
        self.facade.log("Debug message", LogLevel.DEBUG)
        mock_log.assert_called_with(LogLevel.DEBUG, "TestService -> Debug message")

    @patch("logging.Logger.log")
    def test_log__warning_level__logs_warning(self, mock_log):
        self.facade.log("Warning message", LogLevel.WARNING)
        mock_log.assert_called_with(LogLevel.WARNING, "TestService -> Warning message")

    @patch("logging.Logger.log")
    def test_log__error_level__logs_error(self, mock_log):
        self.facade.log("Error message", LogLevel.ERROR)
        mock_log.assert_called_with(LogLevel.ERROR, "TestService -> Error message")

    @patch("logging.Logger.log")
    def test_log__critical_level__logs_critical(self, mock_log):
        self.facade.log("Critical message", LogLevel.CRITICAL)
        mock_log.assert_called_with(LogLevel.CRITICAL, "TestService -> Critical message")

    @patch("logging.Logger.log")
    def test_log__empty_message__does_not_log(self, mock_log):
        self.facade.log("", LogLevel.INFO)
        mock_log.assert_not_called()

    def test_set_level__all_levels__sets_logger_level(self):
        for level in [LogLevel.DEBUG, LogLevel.INFO, LogLevel.WARNING, LogLevel.ERROR, LogLevel.CRITICAL]:
            self.facade.set_level(level)
            self.assertEqual(self.facade._logger.level, level)

    def test_init__default_service__sets_default_service_name(self):
        facade = LoggerFacade()
        self.assertEqual(facade._service, "DefaultService")

    def test_init__custom_service__sets_custom_service_name(self):
        facade = LoggerFacade(service="CustomService")
        self.assertEqual(facade._service, "CustomService")

    def test_init__default_level__sets_default_log_level(self):
        facade = LoggerFacade()
        self.assertEqual(facade._logger.level, LogLevel.INFO)

    def test_init__custom_level__sets_custom_log_level(self):
        facade = LoggerFacade(level=LogLevel.DEBUG)
        self.assertEqual(facade._logger.level, LogLevel.DEBUG)
