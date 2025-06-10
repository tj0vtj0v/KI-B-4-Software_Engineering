import unittest
from unittest.mock import patch

from src.helper.Action import Action
from src.program.DefrostingProgram import DefrostingProgram
from src.user.MockUserInteractionHandler import MockUserInteractionHandler


class TestMockUserInteractionHandler(unittest.TestCase):
    def setUp(self):
        self.handler = MockUserInteractionHandler()

    def tearDown(self):
        self.handler = None

    def test___init__called__creates_instance(self):
        self.assertIsInstance(self.handler, MockUserInteractionHandler)

    def test_get_interactions__first_call__returns_action_and_program(self):
        result = self.handler.get_interactions()

        self.assertEqual(result, (Action.START, DefrostingProgram()))

    def test_get_interactions__subsequent_call__returns_none_tuple(self):
        self.handler.get_interactions()  # First call to set run_once to True
        result = self.handler.get_interactions()

        self.assertEqual(result, (None, None))

    def test_update_display__valid_inputs__executes_without_error(self):
        try:
            self.handler.update_display("Defrosting", running=True, finished=False, paused=False)
        except Exception as e:
            self.fail(f"update_display raised an exception: {e}")

    def test_get_interactions__mocked_run_once__returns_none_tuple(self):
        with patch.object(MockUserInteractionHandler, 'run_once', new=True):
            result = self.handler.get_interactions()

        self.assertEqual(result, (None, None))

    def test_update_display__mocked_method__called_with_correct_arguments(self):
        with patch.object(self.handler, 'update_display', wraps=self.handler.update_display) as mock_update_display:
            self.handler.update_display("Defrosting", running=True, finished=False, paused=False)

            mock_update_display.assert_called_once_with("Defrosting", running=True, finished=False, paused=False)


if __name__ == "__main__":
    unittest.main()
