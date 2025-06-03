import unittest
from unittest.mock import MagicMock

from src.components.door.Door import Door
from src.helper.logging.LogLevel import LogLevel


class TestDoor(unittest.TestCase):
    def test_open__initial_state__opened_is_false(self):
        door = Door()
        self.assertFalse(door.opened)

    def test_singleton_behavior__multiple_instances__same_object(self):
        door1 = Door()
        door2 = Door()

        self.assertIs(door1, door2)
        self.assertIs(door1.logger, door2.logger)
        self.assertEqual(door1.opened, door2.opened)

    def test_open__closed_door__opened_is_true_and_logs_open(self):
        door = Door()
        mock_logger = MagicMock()
        door.logger = mock_logger

        door.open()

        self.assertTrue(door.opened)
        mock_logger.log.assert_called_with("Door is now open.", level=LogLevel.INFO)

    def test_open__already_open_door__logs_already_open(self):
        door = Door()
        mock_logger = MagicMock()
        door.logger = mock_logger

        door.open()
        door.open()

        mock_logger.log.assert_any_call("Door is already open.", level=LogLevel.WARNING)

    def test_close__open_door__opened_is_false_and_logs_closed(self):
        door = Door()
        mock_logger = MagicMock()
        door.logger = mock_logger

        door.open()
        door.close()

        self.assertFalse(door.opened)
        mock_logger.log.assert_any_call("Door is now closed.", level=LogLevel.INFO)

    def test_close__already_closed_door__logs_already_closed(self):
        door = Door()
        mock_logger = MagicMock()
        door.logger = mock_logger

        door.close()

        mock_logger.log.assert_any_call("Door is already closed.", level=LogLevel.WARNING)
