import unittest

import src.helper.exceptions as exceptions


class TestExceptions(unittest.TestCase):
    def test_CustomException__exists_and_is_subclass_of_exception(self):
        self.assertTrue(hasattr(exceptions, "CustomException"))
        self.assertTrue(issubclass(exceptions.CustomException, Exception))

    def test_CustomException__message_passed__message_set_correctly(self):
        message = "Custom exception occurred."
        exception = exceptions.CustomException(message)
        self.assertEqual(str(exception), message)

    def test_MockException__exists_and_is_subclass_of_exception(self):
        self.assertTrue(hasattr(exceptions, "MockException"))
        self.assertTrue(issubclass(exceptions.MockException, exceptions.CustomException))

    def test_MockException__no_arguments__default_message_set(self):
        exception = exceptions.MockException()
        self.assertEqual(str(exception), "This is a mock exception.")

    def test_DoorException__exists_and_is_subclass_of_exception(self):
        self.assertTrue(hasattr(exceptions, "DoorException"))
        self.assertTrue(issubclass(exceptions.DoorException, exceptions.CustomException))

    def test_DoorException__message_passed__message_set_correctly(self):
        message = "Door operation failed."
        exception = exceptions.DoorException(message)
        self.assertEqual(str(exception), message)
