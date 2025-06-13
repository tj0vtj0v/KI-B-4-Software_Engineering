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

        self.system.program_controller = MagicMock()
        self.system.alarm_controller = MagicMock()
        self.system.light_controller = MagicMock()
        self.system.door_controller = MagicMock()
        self.system.sensor_manager = MagicMock()
        self.system.user_interaction_handler = MagicMock()
        self.system.emergency_handler = MagicMock()

    def test___init__called__sets_initial_state_idle(self):
        self.assertEqual(self.system.state, self.system.State.IDLE)

    @patch("src.SystemControl.SystemControl.loop", return_value=None)
    def test_start__idle_state__transitions_to_running(self, mock_loop):
        self.system.start()

        self.assertEqual(self.system.state, self.system.State.RUNNING)

    def test_start__non_idle_state__logs_warning(self):
        self.system.state = self.system.State.RUNNING
        self.system.start()

        self.system.logger.log.assert_called_with("System is already running or in emergency state.", LogLevel.WARNING)

    def test_stop__idle_state__logs_idle_message(self):
        self.system.state = self.system.State.IDLE
        self.system.stop()

        self.system.logger.log.assert_called_with("System is already idle, nothing to shut down", LogLevel.WARNING)

    def test_stop__running_state__resets_components_and_sets_idle(self):
        self.system.state = self.system.State.RUNNING
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
        self.system.alarm_controller.is_alarming.return_value = False
        self.system.declare_emergency()

        self.system.alarm_controller.activate_alarm.assert_called_once()
        self.assertEqual(self.system.state, self.system.State.EMERGENCY)

    def test_declare_emergency__already_in_emergency__logs_message(self):
        self.system.state = self.system.State.EMERGENCY
        self.system.declare_emergency()

        self.system.logger.log.assert_called_with("System is already in emergency state", LogLevel.WARNING)

    def test_loop_action__start_action__starts_program(self):
        self.system.user_interaction_handler.get_interactions.return_value = (Action.START, "Program1")
        self.system.program_controller.is_running.return_value = False
        self.system.door_controller.door.opened = False
        self.system.loop_action()

        self.system.program_controller.start.assert_called_once_with("Program1")

    def test_loop_action__start_action_with_open_door__logs_message(self):
        self.system.user_interaction_handler.get_interactions.return_value = (Action.START, "Program1")
        self.system.program_controller.is_running.return_value = False
        self.system.door_controller.door.opened = True
        self.system.loop_action()

        self.system.logger.log.assert_called_with("Door is open, program will not start", LogLevel.INFO)

    def test_loop_action__stop_action__stops_program(self):
        self.system.user_interaction_handler.get_interactions.return_value = (Action.STOP, None)
        self.system.program_controller.is_running.return_value = True
        self.system.loop_action()

        self.system.program_controller.stop.assert_called_once()

    def test_loop_action__pause_action__pauses_program(self):
        self.system.user_interaction_handler.get_interactions.return_value = (Action.PAUSE, None)
        self.system.program_controller.is_running.return_value = True
        self.system.program_controller.is_paused.return_value = False
        self.system.loop_action()

        self.system.program_controller.pause.assert_called_once()

    def test_loop_action__resume_action__resumes_program(self):
        self.system.user_interaction_handler.get_interactions.return_value = (Action.RESUME, None)
        self.system.program_controller.is_running.return_value = True
        self.system.program_controller.is_paused.return_value = True
        self.system.loop_action()

        self.system.program_controller.resume.assert_called_once()

    def test_emergency_stop_program__called__logs_message_and_stops_program(self):
        self.system.emergency_stop_program()

        self.system.logger.log.assert_called_with("Emergency stopping the program", LogLevel.INFO)
        self.system.program_controller.emergency_stop.assert_called_once()

    def test_loop_action__invalid_action__does_nothing(self):
        self.system.user_interaction_handler.get_interactions.return_value = (None, None)
        self.system.loop_action()

        self.system.program_controller.start.assert_not_called()
        self.system.program_controller.stop.assert_not_called()
