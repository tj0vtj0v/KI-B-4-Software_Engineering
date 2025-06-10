import unittest
from unittest.mock import MagicMock

from src.helper.logging.LogLevel import LogLevel
from src.helper.logging.LoggerInterface import LoggerInterface


class TestLoggerInterface(unittest.TestCase):
    def setUp(self):
        self.mock_logger = MagicMock(spec=LoggerInterface)

    def tearDown(self):
        self.mock_logger = None

    def test___init__call_on_interface__raises_type_error(self):
        with self.assertRaises(TypeError):
            LoggerInterface()

    def test___init__with_subclass_without_implementation__raises_type_error(self):
        class DummyLogger(LoggerInterface):
            pass

        with self.assertRaises(TypeError):
            DummyLogger()

    def test_log__implemented_in_subclass__calls_successfully(self):
        class DummyLogger(LoggerInterface):
            def log(self, message: str, level: LogLevel = LogLevel.INFO) -> None:
                self.called = (message, level)

            def set_level(self, level: LogLevel) -> None:
                self.level = level

        logger = DummyLogger()
        logger.log("msg", LogLevel.ERROR)

        self.assertEqual(logger.called, ("msg", LogLevel.ERROR))

    def test_set_level__implemented_in_subclass__calls_successfully(self):
        class DummyLogger(LoggerInterface):
            def log(self, message: str, level: LogLevel = LogLevel.INFO) -> None:
                pass

            def set_level(self, level: LogLevel) -> None:
                self.level = level

        logger = DummyLogger()
        logger.set_level(LogLevel.DEBUG)

        self.assertEqual(logger.level, LogLevel.DEBUG)

    def test_log__mocked_logger__calls_with_correct_arguments(self):
        self.mock_logger.log("test message", LogLevel.WARNING)

        self.mock_logger.log.assert_called_once_with("test message", LogLevel.WARNING)

    def test_set_level__mocked_logger__sets_correct_level(self):
        self.mock_logger.set_level(LogLevel.CRITICAL)

        self.mock_logger.set_level.assert_called_once_with(LogLevel.CRITICAL)

    def test_log__invalid_message_type__raises_type_error(self):
        class DummyLogger(LoggerInterface):
            def log(self, message: str, level: LogLevel = LogLevel.INFO) -> None:
                if not isinstance(message, str):
                    raise TypeError("Message must be a string")

            def set_level(self, level: LogLevel) -> None:
                pass

        logger = DummyLogger()

        with self.assertRaises(TypeError):
            logger.log(123, LogLevel.INFO)

    def test_set_level__invalid_level_type__raises_type_error(self):
        class DummyLogger(LoggerInterface):
            def log(self, message: str, level: LogLevel = LogLevel.INFO) -> None:
                pass

            def set_level(self, level: LogLevel) -> None:
                if not isinstance(level, LogLevel):
                    raise TypeError("Level must be an instance of LogLevel")

        logger = DummyLogger()

        with self.assertRaises(TypeError):
            logger.set_level("INVALID_LEVEL")
