import unittest
from unittest.mock import MagicMock, patch

from src.emergency.EmergencyHandler import EmergencyHandler
from src.helper.Logger import LogLevel
from src.helper.exceptions import CustomException, MockException, DoorException


class DummySystemControl:
    def __init__(self):
        self.reset_called = False
        self.stop_called = False
        self.alarm_controller = MagicMock()

    def factory_reset(self):
        self.reset_called = True

    def stop(self):
        self.stop_called = True


class TestEmergencyHandler(unittest.TestCase):
    def setUp(self):
        EmergencyHandler.error = None

    def test_observe__normal_flow__returns_result_and_no_error(self):
        class Dummy:
            @EmergencyHandler.observe
            def foo(self, x):
                return x + 1

        d = Dummy()
        self.assertEqual(d.foo(1), 2)
        self.assertIsNone(EmergencyHandler.error)

    def test_observe__invalid_usage__raises_type_error(self):
        @EmergencyHandler.observe
        class Dummy:
            pass

        with self.assertRaises(TypeError):
            Dummy()

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
            def __init__(self):
                self.shutdown_called = False

            @EmergencyHandler.observe
            def foo(self):
                raise ValueError("fail")

            def shutdown(self):
                self.shutdown_called = True

        d = Dummy()
        d.shutdown = MagicMock()

        with patch.object(EmergencyHandler.logger, "log") as log_mock:
            with self.assertRaises(ValueError):
                d.foo()
            log_mock.assert_called()

    def test_alarm_deactivated__when_emergency(self):
        handler = EmergencyHandler()
        handler.error = CustomException("alarm test")
        sys_control = DummySystemControl()
        sys_control.alarm_controller.deactivate_alarm = MagicMock()

        with patch.object(handler.logger, "log"):
            handler.handle_emergency(sys_control)

        sys_control.alarm_controller.deactivate_alarm.assert_called_once()

    def test_is_busy__error_none_and_error_set__returns_false_and_true(self):
        self.assertFalse(EmergencyHandler.is_busy())
        EmergencyHandler.error = CustomException("fail")
        self.assertTrue(EmergencyHandler.is_busy())

    def test_handle_emergency__mock_exception__logs_and_clears_error(self):
        handler = EmergencyHandler()
        handler.error = MockException()
        sys_control = DummySystemControl()
        sys_control.alarm_controller.deactivate_alarm = MagicMock()

        with patch.object(handler.logger, "log") as log_mock:
            handler.handle_emergency(sys_control)
            log_mock.assert_called()

        self.assertIsNone(EmergencyHandler.error)

    def test_handle_emergency__real_exception_and_sys_control__logs_and_resets(self):
        handler = EmergencyHandler()
        handler.error = CustomException("fail")
        sys_control = DummySystemControl()
        sys_control.alarm_controller.deactivate_alarm = MagicMock()

        with patch.object(handler.logger, "log") as log_mock:
            handler.handle_emergency(sys_control)
            log_mock.assert_called()

        self.assertTrue(sys_control.reset_called)
        sys_control.alarm_controller.deactivate_alarm.assert_called_once()

    def test_handle_emergency__door_exception__logs_and_stops_system(self):
        handler = EmergencyHandler()
        handler.error = DoorException("door test")
        sys_control = DummySystemControl()
        sys_control.alarm_controller.deactivate_alarm = MagicMock()

        with patch.object(handler.logger, "log") as log_mock:
            handler.handle_emergency(sys_control)
            log_mock.assert_called()

        self.assertTrue(sys_control.stop_called)
        sys_control.alarm_controller.deactivate_alarm.assert_called_once()

    def test_handle_emergency__no_error__logs_and_resets(self):
        handler = EmergencyHandler()
        handler.error = None
        sys_control = DummySystemControl()
        sys_control.alarm_controller.deactivate_alarm = MagicMock()

        with patch.object(handler.logger, "log") as log_mock:
            handler.handle_emergency(sys_control)
            log_mock.assert_called_with("Resetting system.", level=LogLevel.ERROR)

        self.assertTrue(sys_control.reset_called)
        sys_control.alarm_controller.deactivate_alarm.assert_called_once()
