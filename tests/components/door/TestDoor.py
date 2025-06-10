import unittest
from unittest.mock import MagicMock

from src.components.door.Door import Door
from src.helper.logging.LogLevel import LogLevel


class TestDoor(unittest.TestCase):
    def setUp(self):
        Door._instance = None
        self.door = Door()
        self.mock_logger = MagicMock()
        self.door.logger = self.mock_logger

    def test_open__initial_state__opened_is_false(self):
        self.assertFalse(self.door.opened)

    def test_singleton_behavior__multiple_instances__same_object(self):
        door1 = Door()
        door2 = Door()

        self.assertIs(door1, door2)

    def test_open__closed_door__opened_is_true_and_logs_open(self):
        self.door.open()

        self.assertTrue(self.door.opened)
        self.mock_logger.log.assert_called_with("Door is now open.", LogLevel.INFO)

    def test_open__already_open_door__logs_already_open(self):
        self.door.open()
        self.door.open()

        self.mock_logger.log.assert_any_call("Door is already open.", LogLevel.WARNING)

    def test_close__open_door__opened_is_false_and_logs_closed(self):
        self.door.open()
        self.door.close()

        self.assertFalse(self.door.opened)
        self.mock_logger.log.assert_any_call("Door is now closed.", LogLevel.INFO)

    def test_close__already_closed_door__logs_already_closed(self):
        self.door.close()

        self.mock_logger.log.assert_any_call("Door is already closed.", LogLevel.WARNING)

    def test_open__multiple_calls__logs_correctly(self):
        for _ in range(3):
            self.door.open()

        self.mock_logger.log.assert_any_call("Door is already open.", LogLevel.WARNING)

    def test_close__multiple_calls__logs_correctly(self):
        self.door.open()
        for _ in range(3):
            self.door.close()

        self.mock_logger.log.assert_any_call("Door is already closed.", LogLevel.WARNING)
