# tests/helper/test_exceptions.py
import unittest

import src.helper.exceptions as exceptions


class TestExceptions(unittest.TestCase):
    def test_CustomException__exists_and_is_subclass_of_exception(self):
        self.assertTrue(hasattr(exceptions, "CustomException"))
        self.assertTrue(issubclass(exceptions.CustomException, Exception))

    def test_MockException__exists_and_is_subclass_of_exception(self):
        self.assertTrue(hasattr(exceptions, "MockException"))
        self.assertTrue(issubclass(exceptions.MockException, Exception))
