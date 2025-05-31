import unittest

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
