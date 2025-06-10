import unittest

from src.helper.logging.LogLevel import LogLevel


class TestLogLevel(unittest.TestCase):
    def test_enum__has_expected_members__true(self):
        self.assertTrue(hasattr(LogLevel, "DEBUG"))
        self.assertTrue(hasattr(LogLevel, "INFO"))
        self.assertTrue(hasattr(LogLevel, "WARNING"))
        self.assertTrue(hasattr(LogLevel, "ERROR"))
        self.assertTrue(hasattr(LogLevel, "CRITICAL"))

    def test_enum__has_expected_values__true(self):
        self.assertEqual(LogLevel.DEBUG.value, 10)
        self.assertEqual(LogLevel.INFO.value, 20)
        self.assertEqual(LogLevel.WARNING.value, 30)
        self.assertEqual(LogLevel.ERROR.value, 40)
        self.assertEqual(LogLevel.CRITICAL.value, 50)

    def test_enum_value_initialization__valid_values__returns_expected_member(self):
        self.assertIs(LogLevel(10), LogLevel.DEBUG)
        self.assertIs(LogLevel(20), LogLevel.INFO)
        self.assertIs(LogLevel(30), LogLevel.WARNING)
        self.assertIs(LogLevel(40), LogLevel.ERROR)
        self.assertIs(LogLevel(50), LogLevel.CRITICAL)

    def test_enum_name_initialization_case_insensitive__valid_names__returns_expected_member(self):
        self.assertIs(LogLevel("DEBUG"), LogLevel.DEBUG)
        self.assertIs(LogLevel("debug"), LogLevel.DEBUG)
        self.assertIs(LogLevel("DeBuG"), LogLevel.DEBUG)

        self.assertIs(LogLevel("INFO"), LogLevel.INFO)
        self.assertIs(LogLevel("info"), LogLevel.INFO)
        self.assertIs(LogLevel("InFo"), LogLevel.INFO)

        self.assertIs(LogLevel("WARNING"), LogLevel.WARNING)
        self.assertIs(LogLevel("warning"), LogLevel.WARNING)
        self.assertIs(LogLevel("WarNinG"), LogLevel.WARNING)

        self.assertIs(LogLevel("ERROR"), LogLevel.ERROR)
        self.assertIs(LogLevel("error"), LogLevel.ERROR)
        self.assertIs(LogLevel("ErRoR"), LogLevel.ERROR)

        self.assertIs(LogLevel("CRITICAL"), LogLevel.CRITICAL)
        self.assertIs(LogLevel("critical"), LogLevel.CRITICAL)
        self.assertIs(LogLevel("CrItIcAl"), LogLevel.CRITICAL)

    def test_enum_invalid_name_initialization__invalid_names__raises_value_error(self):
        with self.assertRaises(ValueError):
            LogLevel("NOT_A_LEVEL")

        with self.assertRaises(ValueError):
            LogLevel("")

        with self.assertRaises(ValueError):
            LogLevel(None)

    def test_enum_invalid_value_initialization__invalid_values__raises_value_error(self):
        with self.assertRaises(ValueError):
            LogLevel(0)

        with self.assertRaises(ValueError):
            LogLevel(100)

        with self.assertRaises(ValueError):
            LogLevel(-10)

    def test_enum_missing_method__valid_string_value__returns_expected_member(self):
        self.assertIs(LogLevel._missing_("debug"), LogLevel.DEBUG)
        self.assertIs(LogLevel._missing_("INFO"), LogLevel.INFO)
        self.assertIs(LogLevel._missing_("warning"), LogLevel.WARNING)
        self.assertIs(LogLevel._missing_("ERROR"), LogLevel.ERROR)
        self.assertIs(LogLevel._missing_("critical"), LogLevel.CRITICAL)

    def test_enum_missing_method__invalid_string_value__returns_none(self):
        self.assertIsNone(LogLevel._missing_("not_a_level"))
        self.assertIsNone(LogLevel._missing_(""))
        self.assertIsNone(LogLevel._missing_(None))

    def test_enum_missing_method__non_string_value__returns_none(self):
        self.assertIsNone(LogLevel._missing_(123))
        self.assertIsNone(LogLevel._missing_(object()))
