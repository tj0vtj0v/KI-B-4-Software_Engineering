import unittest
from unittest.mock import MagicMock, patch

from src.SystemControl import SystemControl
from src.helper.exceptions import MockException
from src.helper.logging.LogLevel import LogLevel


class TestSystemControl(unittest.TestCase):
    def setUp(self):
        self.system = SystemControl()

    def test___init__called__sets_initial_state_idle(self):
        self.assertEqual(self.system.state, self.system.State.IDLE)

    def test_start_and_stop__called__transitions_state_correctly(self):
        self.system.program_controller.start = MagicMock()
        self.system.start()
        self.assertEqual(self.system.state, self.system.State.RUNNING)

        self.system.program_controller.stop = MagicMock()
        self.system.stop()
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

    def test_stop__called_while_idle__logs_idle_message(self):
        self.system.state = self.system.State.IDLE

        with patch.object(self.system.logger, "log") as log_mock:
            self.system.stop()
            log_mock.assert_called_with("System is already idle, nothing to shut down.")

    def test_loop_action__mock_exception_raised__emergency_handler_becomes_busy(self):
        self.system.user_interaction_handler.get_interactions = MagicMock()
        self.system.program_controller.update = MagicMock(side_effect=MockException())
        self.system.user_interaction_handler.update_display = MagicMock()

        with patch.object(self.system.emergency_handler.logger, "log"):
            self.system.loop_action()
        self.assertTrue(self.system.emergency_handler.is_busy())

    def test_declare_emergency__starts_alarm(self):
        self.system.alarm_controller.activate_alarm = MagicMock()
        self.system.alarm_controller.is_alarming = MagicMock(return_value=False)
        self.system.state = self.system.State.RUNNING

        self.system.declare_emergency()

        self.system.alarm_controller.activate_alarm.assert_called_once()
        self.assertEqual(self.system.state, self.system.State.EMERGENCY)

    def test_loop__idle_state__logs_idle_and_exits(self):
        self.system.state = self.system.State.IDLE
        with patch.object(self.system.logger, "log") as log_mock:
            self.system.loop()
            log_mock.assert_called_with("System is idle.")

    def test_start__already_running__logs_warning(self):
        self.system.state = self.system.State.RUNNING
        with patch.object(self.system.logger, "log") as log_mock:
            self.system.start()
            log_mock.assert_called_with("System is already running or in emergency state.", level=LogLevel.WARNING)

    def test_factory_reset__reinitializes_components(self):
        with patch.object(self.system, "__init__") as init_mock:
            self.system.factory_reset()
            init_mock.assert_called_once()

    def test_declare_emergency__alarm_already_active__logs_message(self):
        self.system.state = self.system.State.RUNNING
        self.system.alarm_controller.is_alarming = MagicMock(return_value=True)
        with patch.object(self.system.logger, "log") as log_mock:
            self.system.declare_emergency()
            log_mock.assert_called_with("Declaring emergency state.")

    def test_loop_action__exception_in_sensor_update__emergency_handler_becomes_busy(self):
        self.system.sensor_manager.update_sensors = MagicMock(side_effect=MockException())
        self.system.user_interaction_handler.get_interactions = MagicMock()
        self.system.program_controller.update = MagicMock()
        self.system.user_interaction_handler.update_display = MagicMock()

        with patch.object(self.system.emergency_handler.logger, "log"):
            self.system.loop_action()
        self.assertTrue(self.system.emergency_handler.is_busy())

    def test_start__emergency_state__logs_warning_and_does_not_start(self):
        self.system.state = self.system.State.EMERGENCY
        with patch.object(self.system.logger, "log") as log_mock:
            self.system.start()
            log_mock.assert_called_with("System is already running or in emergency state.", level=LogLevel.WARNING)

    def test_stop__running_state__resets_components_and_sets_idle(self):
        self.system.state = self.system.State.RUNNING
        self.system.sensor_manager.reset = MagicMock()
        self.system.program_controller.stop = MagicMock()

        self.system.stop()

        self.system.sensor_manager.reset.assert_called_once()
        self.system.program_controller.stop.assert_called_once()
        self.assertEqual(self.system.state, self.system.State.IDLE)

    def test_factory_reset__emergency_state__resets_to_idle(self):
        self.system.state = self.system.State.EMERGENCY
        self.system.factory_reset()
        self.assertEqual(self.system.state, self.system.State.IDLE)

    def test_declare_emergency__already_in_emergency__logs_message(self):
        self.system.state = self.system.State.EMERGENCY
        with patch.object(self.system.logger, "log") as log_mock:
            self.system.declare_emergency()
            log_mock.assert_called_with("System is already in emergency state.")
