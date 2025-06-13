import sys
import unittest
from unittest.mock import MagicMock, patch

from src.helper.Action import Action
from src.program.DefrostingProgram import DefrostingProgram
from src.user.UserInteractionHandler import UserInteractionHandler

sys.modules['pynput'] = MagicMock()
sys.modules['pynput.keyboard'] = MagicMock()


class TestUserInteractionHandler(unittest.TestCase):
    def setUp(self):
        UserInteractionHandler._instance = None
        self.mock_door = MagicMock()
        self.mock_input_detector = MagicMock()
        self.mock_logger = MagicMock()

        with patch('src.user.UserInteractionHandler.Door', return_value=self.mock_door), \
                patch('src.user.UserInteractionHandler.InputDetector', return_value=self.mock_input_detector), \
                patch('src.user.UserInteractionHandler.Logger', return_value=self.mock_logger):
            self.handler = UserInteractionHandler()

    def test_get_interactions__start_action__returns_action_and_program(self):
        self.mock_input_detector.get_latest_action.return_value = Action.START
        result_action, result_program = self.handler.get_interactions()

        self.assertEqual(result_action, Action.START)
        self.assertIsInstance(result_program, DefrostingProgram)

    def test_get_interactions__open_door_action__opens_door_and_returns_none(self):
        self.mock_input_detector.get_latest_action.return_value = Action.OPEN_DOOR
        self.mock_door.opened = False
        result_action, result_program = self.handler.get_interactions()

        self.mock_door.open.assert_called_once()
        self.assertIsNone(result_action)
        self.assertIsNone(result_program)

    def test_get_interactions__close_door_action__closes_door_and_returns_none(self):
        self.mock_input_detector.get_latest_action.return_value = Action.CLOSE_DOOR
        self.mock_door.opened = True
        result_action, result_program = self.handler.get_interactions()

        self.mock_door.close.assert_called_once()
        self.assertIsNone(result_action)
        self.assertIsNone(result_program)

    def test_get_interactions__unsupported_action__returns_action_and_none(self):
        self.mock_input_detector.get_latest_action.return_value = Action.PAUSE
        result_action, result_program = self.handler.get_interactions()

        self.assertEqual(result_action, Action.PAUSE)
        self.assertIsNone(result_program)

    def test_get_interactions__no_action__returns_none_and_none(self):
        self.mock_input_detector.get_latest_action.return_value = None
        result_action, result_program = self.handler.get_interactions()

        self.assertIsNone(result_action)
        self.assertIsNone(result_program)

    def test_update_display__valid_inputs__does_not_raise_exception(self):
        try:
            self.handler.update_display("ProgramName", running=True, finished=False, paused=False)
        except Exception as e:
            self.fail(f"update_display raised an exception: {e}")
