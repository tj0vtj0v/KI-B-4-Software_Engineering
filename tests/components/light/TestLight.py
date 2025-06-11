import unittest

from src.components.light.Light import Light


class TestLight(unittest.TestCase):
    def setUp(self):
        self.light = None
        self.light = Light()

    def test___new___instance_created__singleton(self):
        instance1 = Light()
        instance2 = Light()

        self.assertIs(instance1, instance2)

    def test___init___default_state__off(self):
        self.assertFalse(self.light.on)

    def test_on__set_to_true__state_changes(self):
        self.light.on = True

        self.assertTrue(self.light.on)

    def test_on__set_to_false__state_changes(self):
        self.light.on = True
        self.light.on = False

        self.assertFalse(self.light.on)


if __name__ == "__main__":
    unittest.main()
