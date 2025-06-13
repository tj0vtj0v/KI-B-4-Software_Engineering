import unittest
from unittest.mock import MagicMock, patch

from src.helper.logging.LogLevel import LogLevel
from src.program.Program import Program


class MockProgram(Program):
    def control_components(self):
        pass


class TestProgram(unittest.TestCase):
    def setUp(self):
        self.program = MockProgram()
        self.program.logger = MagicMock()
        self.program.door = MagicMock()
        self.program.magnetron = MagicMock()
        self.program.cooling_fan = MagicMock()
        self.program.turntable = MagicMock()
        self.program.reflector = MagicMock()
        self.program.components = [
            self.program.magnetron,
            self.program.cooling_fan,
            self.program.turntable,
            self.program.reflector,
        ]

    def tearDown(self):
        del self.program

    def test_get_name__default_name__returns_program(self):
        result = self.program.get_name()

        self.assertEqual(result, "Program")

    def test_start__initial_conditions__starts_components_and_control_loop(self):
        self.program.control_loop = MagicMock(side_effect=lambda: setattr(self.program, "finished", True))

        self.program.start()

        self.program.logger.log.assert_any_call("Program is starting", LogLevel.INFO)
        self.program.door.lock.assert_called_once()
        self.program.magnetron.start.assert_called_once()
        self.program.cooling_fan.start.assert_called_once()

    def test_pause__running_program__sets_paused_to_true(self):
        self.program.pause()

        self.assertTrue(self.program.paused)
        self.program.logger.log.assert_called_once_with("Pausing Program", LogLevel.INFO)

    def test_resume__paused_program__sets_paused_to_false_and_notifies(self):
        with patch.object(self.program.pause_condition, "notify_all") as mock_notify:
            self.program.resume()

            self.assertFalse(self.program.paused)
            mock_notify.assert_called_once()
            self.program.logger.log.assert_called_once_with("Resuming Program", LogLevel.INFO)

    def test_stop__running_program__stops_program_and_unlocks_door(self):
        self.program.stop()

        self.assertTrue(self.program.paused)
        self.assertFalse(self.program.running)
        self.program.logger.log.assert_called_once_with("Stopping Program", LogLevel.INFO)

    def test_emergency_stop__running_program__stops_all_components_and_unlocks_door(self):
        self.program.emergency_stop()

        calls = [
            unittest.mock.call("Emergency stopping Program", LogLevel.INFO),
            unittest.mock.call("Stopping Program", LogLevel.INFO),
        ]
        self.program.logger.log.assert_has_calls(calls, any_order=False)

        for component in self.program.components:
            component.emergency_stop.assert_called_once()
        self.program.door.unlock.assert_called_once()

    def test_stop_components__running_program__stops_all_components_and_unlocks_door(self):
        self.program.stop_components()

        self.program.logger.log.assert_called_once_with("Stopping all components from Program", LogLevel.INFO)
        for component in self.program.components:
            component.stop.assert_called_once()
        self.program.door.unlock.assert_called_once()

    def test_control_loop__not_paused_or_finished__calls_control_components_and_updates(self):
        self.program.paused = False
        self.program.finished = False
        self.program.control_components = MagicMock()
        self.program.turntable.update = MagicMock()
        self.program.reflector.update = MagicMock()

        with patch("time.sleep", return_value=None):
            with patch.object(self.program, "control_components",
                              side_effect=lambda: setattr(self.program, "finished", True)):
                self.program.control_loop()

        self.program.turntable.update.assert_called_once()
        self.program.reflector.update.assert_called_once()
