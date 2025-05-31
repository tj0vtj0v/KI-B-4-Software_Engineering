import unittest

from src.user.MockUserInteractionHandler import MockUserInteractionHandler


class TestMockUserInteractionHandler(unittest.TestCase):
    def setUp(self):
        self.handler = MockUserInteractionHandler()

    def test___init__called__creates_instance(self):
        self.assertIsInstance(self.handler, MockUserInteractionHandler)

    def test_get_interactions__exists__is_callable(self):
        self.assertTrue(hasattr(self.handler, "get_interactions"))
        self.assertTrue(callable(getattr(self.handler, "get_interactions", None)))

    def test_update_display__exists__is_callable(self):
        self.assertTrue(hasattr(self.handler, "update_display"))
        self.assertTrue(callable(getattr(self.handler, "update_display", None)))
