import unittest
from unittest.mock import MagicMock, patch

from src.SystemControl import SystemControl
from src.helper.exceptions import MockException


class TestSystemControl(unittest.TestCase):
    def setUp(self):
        self.system = SystemControl()

    def test___init__called__sets_initial_state_idle(self):
        self.assertEqual(self.system.state, self.system.State.IDLE)

    def test_start_and_shutdown__called__transitions_state_correctly(self):
        self.system.program_controller.start = MagicMock()
        self.system.start()
        self.assertEqual(self.system.state, self.system.State.RUNNING)

        self.system.program_controller.stop = MagicMock()
        self.system.shutdown()
        self.assertEqual(self.system.state, self.system.State.IDLE)

    def test_factory_reset__called_while_running__resets_to_idle(self):
        self.system.state = self.system.State.RUNNING
        self.system.factory_reset()

        self.assertEqual(self.system.state, self.system.State.IDLE)

    def test_declare_emergency__called_twice__sets_state_and_logs_warning(self):
        self.system.state = self.system.State.RUNNING
        self.system.declare_emergency()

        self.assertEqual(self.system.state, self.system.State.EMERGENCY)

        with patch.object(self.system.logger, "log") as log_mock:
            self.system.declare_emergency()
            log_mock.assert_called()

    def test_shutdown__called_while_idle__logs_idle_message(self):
        self.system.state = self.system.State.IDLE

        with patch.object(self.system.logger, "log") as log_mock:
            self.system.shutdown()
            log_mock.assert_called_with("System is already idle, nothing to shut down.")

    def test_loop_action__mock_exception_raised__emergency_handler_becomes_busy(self):
        self.system.user_interaction_handler.get_interactions = MagicMock()
        self.system.program_controller.update = MagicMock(side_effect=MockException())
        self.system.user_interaction_handler.update_display = MagicMock()

        with patch.object(self.system.emergency_handler.logger, "log"):
            self.system.loop_action()
        self.assertTrue(self.system.emergency_handler.is_busy())
