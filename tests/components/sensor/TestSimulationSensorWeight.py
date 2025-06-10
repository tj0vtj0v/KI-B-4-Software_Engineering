import unittest
from unittest.mock import MagicMock, patch

from src.components.sensor.SimulationSensorWeight import SimulationSensorWeight
from src.helper.config import TURNTABLE_WEIGHT_IN_GRAMS


class TestSimulationSensorWeight(unittest.TestCase):
    def setUp(self):
        SimulationSensorWeight._instance = None
        self.sensor = SimulationSensorWeight()

    def test_get__initial_weight__returns_default_weight(self):
        self.assertEqual(self.sensor.get(), TURNTABLE_WEIGHT_IN_GRAMS)

    def test_update__door_opened__increases_weight(self):
        self.sensor.door = MagicMock()
        self.sensor.door.opened = True
        self.sensor.last_door_opened = False

        self.sensor.update()

        self.assertGreater(self.sensor.get(), TURNTABLE_WEIGHT_IN_GRAMS)

    def test_update__door_closed__weight_fluctuates(self):
        self.sensor.door = MagicMock()
        self.sensor.door.opened = False
        initial_weight = self.sensor.get()

        with patch("random.uniform", return_value=0.05):
            self.sensor.update()

        self.assertAlmostEqual(self.sensor.get(), initial_weight + 0.05, places=2)

    def test_update__door_reopened__weight_increases_correctly(self):
        self.sensor.door = MagicMock()
        self.sensor.door.opened = True
        self.sensor.last_door_opened = False

        self.sensor.update()
        first_update_weight = self.sensor.get()

        self.sensor.door.opened = False
        self.sensor.update()

        self.sensor.door.opened = True
        self.sensor.update()

        self.assertGreater(self.sensor.get(), first_update_weight)

    def test_reset__after_updates__resets_to_default_weight(self):
        self.sensor.door = MagicMock()
        self.sensor.door.opened = True
        self.sensor.last_door_opened = False

        self.sensor.update()
        self.sensor.reset()

        self.assertEqual(self.sensor.get(), TURNTABLE_WEIGHT_IN_GRAMS)

    def test_update__door_never_opened__weight_fluctuates_only(self):
        self.sensor.door = MagicMock()
        self.sensor.door.opened = False
        initial_weight = self.sensor.get()

        with patch("random.uniform", return_value=-0.05):
            self.sensor.update()

        self.assertAlmostEqual(self.sensor.get(), initial_weight - 0.05, places=2)

    def test_update__door_state_unchanged__weight_fluctuates(self):
        self.sensor.door = MagicMock()
        self.sensor.door.opened = False
        self.sensor.last_door_opened = False
        initial_weight = self.sensor.get()

        with patch("random.uniform", return_value=0.02):
            self.sensor.update()

        self.assertAlmostEqual(self.sensor.get(), initial_weight + 0.02, places=2)

    def test_get__after_multiple_updates__returns_correct_weight(self):
        self.sensor.door = MagicMock()
        self.sensor.door.opened = True
        self.sensor.last_door_opened = False

        self.sensor.update()
        first_update_weight = self.sensor.get()

        self.sensor.door.opened = False
        with patch("random.uniform", return_value=0.03):
            self.sensor.update()

        second_update_weight = self.sensor.get()

        self.assertGreater(first_update_weight, TURNTABLE_WEIGHT_IN_GRAMS)
        self.assertAlmostEqual(second_update_weight, first_update_weight + 0.03, places=2)

    def test_reset__without_prior_updates__resets_to_default_weight(self):
        self.sensor.reset()

        self.assertEqual(self.sensor.get(), TURNTABLE_WEIGHT_IN_GRAMS)

    def test_update__multiple_fluctuations__weight_changes_correctly(self):
        self.sensor.door = MagicMock()
        self.sensor.door.opened = False
        initial_weight = self.sensor.get()

        fluctuations = [0.1, -0.05, 0.03]
        for fluctuation in fluctuations:
            with patch("random.uniform", return_value=fluctuation):
                self.sensor.update()

        expected_weight = initial_weight + sum(fluctuations)
        self.assertAlmostEqual(self.sensor.get(), expected_weight, places=2)
