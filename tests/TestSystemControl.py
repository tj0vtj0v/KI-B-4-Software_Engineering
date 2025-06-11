import unittest
from unittest.mock import MagicMock, patch

from src.SystemControl import SystemControl
from src.helper.Action import Action
from src.helper.logging.LogLevel import LogLevel


class TestSystemControl(unittest.TestCase):
    def setUp(self):
        SystemControl._instance = None
        self.system = SystemControl()
        self.system.logger = MagicMock()

        mock_program = MagicMock()
        mock_program.get_name.return_value = "MockProgram"
        self.system.program_controller.get_running_program = MagicMock(return_value=mock_program)
        self.system.program_controller.is_running = MagicMock(return_value=False)
        self.system.program_controller.is_finished = MagicMock(return_value=False)
        self.system.program_controller.is_paused = MagicMock(return_value=False)
        self.system.user_interaction_handler.update_display = MagicMock()

    def test___init__called__sets_initial_state_idle(self):
        self.assertEqual(self.system.state, self.system.State.IDLE)

    @patch("src.SystemControl.SystemControl.loop", return_value=None)
    def test_start__idle_state__transitions_to_running(self, mock_loop):
        self.system.logger.log = MagicMock()
        self.system.start()

        self.assertEqual(self.system.state, self.system.State.RUNNING)

    def test_start__non_idle_state__logs_warning(self):
        self.system.state = self.system.State.RUNNING
        with patch.object(self.system.logger, "log") as log_mock:
            self.system.start()

            log_mock.assert_called_with("System is already running or in emergency state.", LogLevel.WARNING)

    def test_stop__idle_state__logs_idle_message(self):
        self.system.state = self.system.State.IDLE
        with patch.object(self.system.logger, "log") as log_mock:
            self.system.stop()

            log_mock.assert_called_with("System is already idle, nothing to shut down", LogLevel.WARNING)

    def test_stop__running_state__resets_components_and_sets_idle(self):
        self.system.state = self.system.State.RUNNING
        self.system.sensor_manager.reset = MagicMock()
        self.system.program_controller.stop = MagicMock()
        self.system.light_controller.stop = MagicMock()
        self.system.stop()

        self.system.sensor_manager.reset.assert_called_once()
        self.system.program_controller.stop.assert_called_once()
        self.system.light_controller.stop.assert_called_once()
        self.assertEqual(self.system.state, self.system.State.IDLE)

    def test_factory_reset__called__reinitializes_system(self):
        with patch.object(self.system, "__init__") as init_mock:
            self.system.factory_reset()

            init_mock.assert_called_once()

    def test_declare_emergency__non_emergency_state__activates_alarm_and_sets_emergency(self):
        self.system.state = self.system.State.RUNNING
        self.system.alarm_controller.activate_alarm = MagicMock()
        self.system.alarm_controller.is_alarming = MagicMock(return_value=False)
        self.system.declare_emergency()

        self.system.alarm_controller.activate_alarm.assert_called_once()
        self.assertEqual(self.system.state, self.system.State.EMERGENCY)

    def test_declare_emergency__already_in_emergency__logs_message(self):
        self.system.state = self.system.State.EMERGENCY
        with patch.object(self.system.logger, "log") as log_mock:
            self.system.declare_emergency()

            log_mock.assert_called_with("System is already in emergency state", LogLevel.WARNING)

    def test_loop_action__start_action__starts_program(self):
        self.system.user_interaction_handler.get_interactions = MagicMock(return_value=(Action.START, "Program1"))
        self.system.program_controller.is_running = MagicMock(return_value=False)
        self.system.program_controller.start = MagicMock()
        self.system.loop_action()

        self.system.program_controller.start.assert_called_once_with("Program1")

    def test_loop_action__stop_action__stops_program(self):
        self.system.user_interaction_handler.get_interactions = MagicMock(return_value=(Action.STOP, None))
        self.system.program_controller.is_running = MagicMock(return_value=True)
        self.system.program_controller.stop = MagicMock()
        self.system.loop_action()

        self.system.program_controller.stop.assert_called_once()

    def test_loop_action__pause_action__pauses_program(self):
        self.system.user_interaction_handler.get_interactions = MagicMock(return_value=(Action.PAUSE, None))
        self.system.program_controller.is_running = MagicMock(return_value=True)
        self.system.program_controller.is_paused = MagicMock(return_value=False)
        self.system.program_controller.pause = MagicMock()
        self.system.loop_action()

        self.system.program_controller.pause.assert_called_once()

    def test_loop_action__resume_action__resumes_program(self):
        self.system.user_interaction_handler.get_interactions = MagicMock(return_value=(Action.RESUME, None))
        self.system.program_controller.is_running = MagicMock(return_value=True)
        self.system.program_controller.is_paused = MagicMock(return_value=True)
        self.system.program_controller.resume = MagicMock()
        self.system.loop_action()

        self.system.program_controller.resume.assert_called_once()

    def test_emergency_stop_program__called__logs_message_and_stops_program(self):
        self.system.program_controller.emergency_stop = MagicMock()
        with patch.object(self.system.logger, "log") as log_mock:
            self.system.emergency_stop_program()

            log_mock.assert_called_with("Emergency stopping the program", LogLevel.INFO)
            self.system.program_controller.emergency_stop.assert_called_once()
