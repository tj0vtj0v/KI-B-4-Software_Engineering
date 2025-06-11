import unittest
from unittest.mock import MagicMock

from src.helper.Logger import Logger
from src.helper.logging.LogLevel import LogLevel
from src.program.Program import Program
from src.program.ProgramController import ProgramController


class TestProgramController(unittest.TestCase):
    def setUp(self):
        ProgramController._instance = None
        self.program_controller = ProgramController()
        self.mock_program = MagicMock(spec=Program)
        self.program_controller.logger = MagicMock(spec=Logger)

    def tearDown(self):
        self.mock_program = None

    def test_start__valid_program__starts_thread(self):
        self.mock_program.get_name.return_value = "TestProgram"
        self.program_controller.start(self.mock_program)

        self.program_controller.logger.log.assert_called_once_with(
            "Starting program: TestProgram", LogLevel.INFO
        )
        self.assertTrue(self.program_controller.thread)

    def test_pause__valid_program__logs_and_pauses(self):
        self.program_controller.program = self.mock_program
        self.mock_program.name = "TestProgram"
        self.program_controller.pause()

        self.program_controller.logger.log.assert_called_once_with(
            "Pausing program: TestProgram", LogLevel.INFO
        )
        self.mock_program.pause.assert_called_once()

    def test_resume__valid_program__logs_and_resumes(self):
        self.program_controller.program = self.mock_program
        self.mock_program.name = "TestProgram"
        self.program_controller.resume()

        self.program_controller.logger.log.assert_called_once_with(
            "Resuming program: TestProgram", LogLevel.INFO
        )
        self.mock_program.resume.assert_called_once()

    def test_stop__valid_program__logs_and_stops(self):
        self.program_controller.program = self.mock_program
        self.mock_program.name = "TestProgram"
        self.program_controller.stop()

        self.program_controller.logger.log.assert_called_once_with(
            "Stopping program: TestProgram", LogLevel.INFO
        )
        self.mock_program.stop.assert_called_once()

    def test_emergency_stop__valid_program__logs_and_emergency_stops(self):
        self.program_controller.program = self.mock_program
        self.mock_program.name = "TestProgram"
        self.program_controller.emergency_stop()

        self.program_controller.logger.log.assert_called_once_with(
            "Emergency stopping program: TestProgram", LogLevel.INFO
        )
        self.mock_program.emergency_stop.assert_called_once()

    def test_is_running__program_running__returns_true(self):
        self.program_controller.program = self.mock_program
        self.mock_program.running = True
        result = self.program_controller.is_running()

        self.assertTrue(result)

    def test_is_running__no_program__returns_false(self):
        self.program_controller.program = None
        result = self.program_controller.is_running()

        self.assertFalse(result)

    def test_is_finished__program_finished__returns_true(self):
        self.program_controller.program = self.mock_program
        self.mock_program.finished = True
        result = self.program_controller.is_finished()

        self.assertTrue(result)

    def test_is_paused__program_paused__returns_true(self):
        self.program_controller.program = self.mock_program
        self.mock_program.paused = True
        result = self.program_controller.is_paused()

        self.assertTrue(result)

    def test_get_running_program__valid_program__returns_name(self):
        self.program_controller.program = self.mock_program
        self.mock_program.get_name.return_value = "TestProgram"
        result = self.program_controller.get_running_program()

        self.assertEqual(result, "TestProgram")

    def test_get_running_program__no_program__returns_default_message(self):
        self.program_controller.program = None
        result = self.program_controller.get_running_program()

        self.assertEqual(result, "No program running")

    def test_get_state_tuple__valid_program__returns_correct_tuple(self):
        self.program_controller.program = self.mock_program
        self.mock_program.get_name.return_value = "TestProgram"
        self.mock_program.running = True
        self.mock_program.finished = False
        self.mock_program.paused = False
        result = self.program_controller.get_state_tuple()

        self.assertEqual(result, ("TestProgram", True, False, False))

    def test_get_state_tuple__no_program__returns_default_tuple(self):
        self.program_controller.program = None
        result = self.program_controller.get_state_tuple()

        self.assertEqual(result, ("No program running", False, True, False))
