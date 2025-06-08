import unittest

from src.helper.logging.LogLevel import LogLevel
from src.helper.logging.LoggerInterface import LoggerInterface


class TestLoggerInterface(unittest.TestCase):
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
