import unittest
from unittest.mock import MagicMock

from src.components.door.DoorController import DoorController
from src.helper.exceptions import DoorException
from src.helper.logging.LogLevel import LogLevel


class TestDoorController(unittest.TestCase):
    def setUp(self):
        DoorController._instance = None
        self.controller = DoorController()
        self.mock_logger = MagicMock()
        self.controller.logger = self.mock_logger

    def test_singleton_instance__multiple_instances__same_object(self):
        instance1 = DoorController()
        instance2 = DoorController()

        self.assertIs(instance1, instance2)

    def test_lock__door_closed__locks_and_logs(self):
        self.controller.door.opened = False
        self.controller.lock()

        self.assertTrue(self.controller.locked)
        self.mock_logger.log.assert_called_with("Door is now locked.", level=LogLevel.INFO)

    def test_lock__door_open__warns_and_does_not_lock(self):
        self.controller.door.opened = True
        self.controller.lock()

        self.assertFalse(self.controller.locked)
        self.mock_logger.log.assert_called_with("Cannot lock the door while it is open.", level=LogLevel.WARNING)

    def test_lock__already_locked__logs_no_action(self):
        self.controller.door.opened = False
        self.controller.locked = True
        self.controller.lock()

        self.assertTrue(self.controller.locked)
        self.mock_logger.log.assert_called_with("Door is already locked.", level=LogLevel.INFO)

    def test_unlock__door_closed__unlocks_and_logs(self):
        self.controller.door.opened = False
        self.controller.locked = True
        self.controller.unlock()

        self.assertFalse(self.controller.locked)
        self.mock_logger.log.assert_called_with("Door is now unlocked.", level=LogLevel.INFO)

    def test_unlock__door_open__warns_and_does_not_unlock(self):
        self.controller.door.opened = True
        self.controller.locked = True
        self.controller.unlock()

        self.assertTrue(self.controller.locked)
        self.mock_logger.log.assert_called_with("Cannot unlock the door while it is open.", level=LogLevel.WARNING)

    def test_unlock__already_unlocked__logs_no_action(self):
        self.controller.door.opened = False
        self.controller.locked = False
        self.controller.unlock()

        self.assertFalse(self.controller.locked)
        self.mock_logger.log.assert_called_with("Door is already unlocked.", level=LogLevel.INFO)

    def test_check__locked_and_opened__raises_exception(self):
        self.controller.door.opened = True
        self.controller.locked = True

        with self.assertRaises(DoorException) as context:
            self.controller.check()
        self.assertEqual(str(context.exception), "Door is locked and was forcefully opened.")

    def test_check__locked_and_closed__no_exception(self):
        self.controller.door.opened = False
        self.controller.locked = True
        self.controller.check()

    def test_check__unlocked_and_opened__no_exception(self):
        self.controller.door.opened = True
        self.controller.locked = False
        self.controller.check()

    def test_integration_lock_unlock_check__various_states__expected_behaviors(self):
        class DummyDoor:
            def __init__(self):
                self.opened = False

        door = DummyDoor()
        self.controller.door = door

        self.controller.lock()
        self.assertTrue(self.controller.locked)
        self.controller.unlock()
        self.assertFalse(self.controller.locked)

        door.opened = True
        self.controller.lock()
        self.mock_logger.log.assert_called_with("Cannot lock the door while it is open.", level=LogLevel.WARNING)
