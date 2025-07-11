import unittest

from src.helper.Action import Action


class TestAction(unittest.TestCase):
    def test_action__valid_enum_values__correctly_assigned(self):
        self.assertEqual(Action.START.value, "START")
        self.assertEqual(Action.STOP.value, "STOP")
        self.assertEqual(Action.PAUSE.value, "PAUSE")
        self.assertEqual(Action.RESUME.value, "RESUME")
        self.assertEqual(Action.OFF.value, "OFF")
        self.assertEqual(Action.OPEN_DOOR.value, "OPEN_DOOR")
        self.assertEqual(Action.CLOSE_DOOR.value, "CLOSE_DOOR")

    def test_action__invalid_enum_access__raises_attribute_error(self):
        with self.assertRaises(AttributeError):
            _ = Action.INVALID

    def test_action__comparison_with_string__returns_true(self):
        self.assertTrue(Action.START == "START")
        self.assertTrue(Action.STOP == "STOP")
        self.assertTrue(Action.PAUSE == "PAUSE")
        self.assertTrue(Action.RESUME == "RESUME")
        self.assertTrue(Action.OFF == "OFF")
        self.assertTrue(Action.OPEN_DOOR == "OPEN_DOOR")
        self.assertTrue(Action.CLOSE_DOOR == "CLOSE_DOOR")

    def test_action__comparison_with_other_enum__returns_false(self):
        self.assertFalse(Action.START == Action.STOP)
        self.assertFalse(Action.PAUSE == Action.RESUME)
        self.assertFalse(Action.OPEN_DOOR == Action.CLOSE_DOOR)

    def test_action__iteration__returns_all_enum_members(self):
        actions = [action for action in Action]

        self.assertEqual(
            actions,
            [
                Action.START,
                Action.STOP,
                Action.PAUSE,
                Action.RESUME,
                Action.OFF,
                Action.OPEN_DOOR,
                Action.CLOSE_DOOR,
            ],
        )
