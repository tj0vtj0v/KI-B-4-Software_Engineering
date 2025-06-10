import unittest

from src.components.magnetron.Magnetron import Magnetron


class TestMagnetron(unittest.TestCase):
    def setUp(self):
        Magnetron._instance = None
        self.magnetron = Magnetron()

    def test_singleton__multiple_instances__same_object(self):
        magnetron_1 = Magnetron()
        magnetron_2 = Magnetron()

        self.assertIs(magnetron_1, magnetron_2, "Magnetron should be a singleton")

    def test_active__initial_state__is_false(self):
        self.assertFalse(self.magnetron.active, "Magnetron should be inactive initially")

    def test_turn_on__inactive_state__activates_magnetron(self):
        self.magnetron.turn_on()

        self.assertTrue(self.magnetron.active, "Magnetron should be active after turning on")

    def test_turn_off__active_state__deactivates_magnetron(self):
        self.magnetron.turn_on()
        self.magnetron.turn_off()

        self.assertFalse(self.magnetron.active, "Magnetron should be inactive after turning off")

    def test_turn_on__already_active__remains_active(self):
        self.magnetron.turn_on()
        self.magnetron.turn_on()

        self.assertTrue(self.magnetron.active, "Magnetron should remain active if already active")

    def test_turn_off__already_inactive__remains_inactive(self):
        self.magnetron.turn_off()

        self.assertFalse(self.magnetron.active, "Magnetron should remain inactive if already inactive")
