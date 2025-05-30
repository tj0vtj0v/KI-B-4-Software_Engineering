import unittest

from src.helper.logging.LogLevel import LogLevel


class TestLogLevel(unittest.TestCase):
    def test__enum__has_expected_members(self):
        self.assertTrue(hasattr(LogLevel, "DEBUG"))
        self.assertTrue(hasattr(LogLevel, "INFO"))
        self.assertTrue(hasattr(LogLevel, "WARNING"))
        self.assertTrue(hasattr(LogLevel, "ERROR"))
        self.assertTrue(hasattr(LogLevel, "CRITICAL"))

    def test__enum__has_expected_values(self):
        self.assertEqual(LogLevel.DEBUG.value, 10)
        self.assertEqual(LogLevel.INFO.value, 20)
        self.assertEqual(LogLevel.WARNING.value, 30)
        self.assertEqual(LogLevel.ERROR.value, 40)
        self.assertEqual(LogLevel.CRITICAL.value, 50)

    def test__enum__value_initialization__returns_expected_member(self):
        self.assertIs(LogLevel(10), LogLevel.DEBUG)
        self.assertIs(LogLevel(20), LogLevel.INFO)
        self.assertIs(LogLevel(30), LogLevel.WARNING)
        self.assertIs(LogLevel(40), LogLevel.ERROR)
        self.assertIs(LogLevel(50), LogLevel.CRITICAL)

    def test__enum__name_initialization_case_insensitive__returns_expected_member(self):
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

    def test__enum__invalid_name_initialization__raises_value_error(self):
        with self.assertRaises(ValueError):
            LogLevel("NOT_A_LEVEL")

        with self.assertRaises(ValueError):
            LogLevel("")

        with self.assertRaises(ValueError):
            LogLevel(None)
