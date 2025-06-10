import unittest
from unittest.mock import MagicMock, patch

from src.emergency.EmergencyHandler import EmergencyHandler
from src.helper.Logger import LogLevel
from src.helper.exceptions import CustomException, MockException, DoorException, ProgramAlreadyRunningException


class DummySystemControl:
    def __init__(self):
        self.reset_called = False
        self.stop_called = False
        self.emergency_stop_called = False
        self.alarm_controller = MagicMock()

    def factory_reset(self):
        self.reset_called = True

    def stop(self):
        self.stop_called = True

    def emergency_stop_program(self):
        self.emergency_stop_called = True


class TestEmergencyHandler(unittest.TestCase):
    def setUp(self):
        EmergencyHandler._instance = None
        self.handler = EmergencyHandler()
        self.system_control = DummySystemControl()

    def tearDown(self):
        EmergencyHandler.error = None

    def test_observe__normal_flow__returns_result_and_no_error(self):
        class Dummy:
            @EmergencyHandler.observe
            def foo(self, x):
                return x + 1

        d = Dummy()

        self.assertEqual(d.foo(1), 2)
        self.assertIsNone(EmergencyHandler.error)

    def test_observe__custom_exception_raised__calls_declare_emergency_and_logs(self):
        class Dummy:
            def __init__(self):
                self.emergency = False

            @EmergencyHandler.observe
            def foo(self):
                raise CustomException("fail")

            def declare_emergency(self):
                self.emergency = True

        d = Dummy()
        d.declare_emergency = MagicMock()

        with patch.object(EmergencyHandler.logger, "log") as log_mock:
            d.foo()
            d.declare_emergency.assert_called_once()
            log_mock.assert_called()

        self.assertIsInstance(EmergencyHandler.error, CustomException)

    def test_observe__generic_exception_raised__reraises_and_logs(self):
        class Dummy:
            @EmergencyHandler.observe
            def foo(self):
                raise ValueError("fail")

        d = Dummy()

        with patch.object(EmergencyHandler.logger, "log") as log_mock:
            with self.assertRaises(ValueError):
                d.foo()

            log_mock.assert_called()

    def test_is_busy__error_none_and_error_set__returns_false_and_true(self):
        self.assertFalse(EmergencyHandler.is_busy())
        EmergencyHandler.error = CustomException("fail")

        self.assertTrue(EmergencyHandler.is_busy())

    def test_handle_emergency__mock_exception__logs_and_clears_error(self):
        self.handler.error = MockException()
        with patch.object(self.handler.logger, "log") as log_mock:
            self.handler.handle_emergency(self.system_control)

            log_mock.assert_called()
        self.assertIsNone(EmergencyHandler.error)

    def test_handle_emergency__door_exception__logs_and_stops_system(self):
        self.handler.error = DoorException("door test")
        with patch.object(self.handler.logger, "log") as log_mock:
            self.handler.handle_emergency(self.system_control)

            log_mock.assert_called()
        self.assertTrue(self.system_control.emergency_stop_called)
        self.system_control.alarm_controller.deactivate_alarm.assert_called_once()

    def test_handle_emergency__program_already_running_exception__logs_and_clears_error(self):
        self.handler.error = ProgramAlreadyRunningException()

        with patch.object(self.handler.logger, "log") as log_mock:
            self.handler.handle_emergency(self.system_control)

            log_mock.assert_called()
        self.assertIsNone(EmergencyHandler.error)

    def test_handle_emergency__no_error__logs_and_resets(self):
        self.handler.error = None
        with patch.object(self.handler.logger, "log") as log_mock:
            self.handler.handle_emergency(self.system_control)

            log_mock.assert_called_with("Resetting system.", LogLevel.ERROR)
        self.assertTrue(self.system_control.reset_called)
        self.system_control.alarm_controller.deactivate_alarm.assert_called_once()

    def test_handle_emergency__real_error__logs_and_resets(self):
        self.handler.error = CustomException("real error")
        with patch.object(self.handler.logger, "log") as log_mock:
            self.handler.handle_emergency(self.system_control)

            log_mock.assert_called_with("Resetting system.", LogLevel.ERROR)
        self.assertTrue(self.system_control.reset_called)
        self.system_control.alarm_controller.deactivate_alarm.assert_called_once()
