import unittest

from src.helper.exceptions import MockException
from src.program.MockProgramController import MockProgramController


class TestMockProgramController(unittest.TestCase):
    def setUp(self):
        self.controller = MockProgramController()

    def test___init__called__creates_inactive_instance(self):
        self.assertIsInstance(self.controller, MockProgramController)
        self.assertFalse(self.controller.active)

    def test_start__called__sets_active_true(self):
        self.controller.start()
        self.assertTrue(self.controller.active)

    def test_update__after_start_called__does_not_raise(self):
        self.controller.start()
        try:
            self.controller.update()
        except AssertionError:
            self.fail("update() raised AssertionError unexpectedly!")

    def test_update__without_start_called__raises_assertion_error(self):
        with self.assertRaises(AssertionError):
            self.controller.update()

    def test_mock_error__called__raises_mock_exception(self):
        with self.assertRaises(MockException):
            self.controller.mock_error()

    def test_stop__after_start_and_update__sets_active_false(self):
        self.controller.start()
        self.assertTrue(self.controller.active)

        try:
            self.controller.update()
        except AssertionError:
            self.fail("update() raised AssertionError unexpectedly!")

        self.controller.stop()
        self.assertFalse(self.controller.active)

    def test_start_and_stop__called_multiple_times__maintains_idempotency(self):
        self.controller.start()
        self.assertTrue(self.controller.active)
        self.controller.start()
        self.assertTrue(self.controller.active)
        self.controller.stop()
        self.assertFalse(self.controller.active)
        self.controller.stop()
        self.assertFalse(self.controller.active)
