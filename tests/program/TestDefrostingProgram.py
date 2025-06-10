import unittest
from unittest.mock import MagicMock

from src.helper.config import TURNTABLE_WEIGHT_IN_GRAMS, AMBIENT_TEMPERATURE_IN_CELSIUS, PROGRAM_DEFROSTING_TARGET_TEMP
from src.program.DefrostingProgram import DefrostingProgram


class TestDefrostingProgram(unittest.TestCase):

    def setUp(self):
        self.mock_sensors = MagicMock()
        self.mock_logger = MagicMock()
        self.mock_magnetron = MagicMock()
        self.mock_turntable = MagicMock()

        DefrostingProgram._instance = None
        self.program = DefrostingProgram()
        self.program.sensors = self.mock_sensors
        self.program.logger = self.mock_logger
        self.program.magnetron = self.mock_magnetron
        self.program.turntable = self.mock_turntable

        self.mock_sensors.inner_weight.return_value = TURNTABLE_WEIGHT_IN_GRAMS
        self.mock_sensors.inner_temp1.return_value = AMBIENT_TEMPERATURE_IN_CELSIUS
        self.mock_sensors.inner_temp2.return_value = AMBIENT_TEMPERATURE_IN_CELSIUS

    def test___new____singleton_behavior__returns_same_instance(self):
        instance1 = DefrostingProgram()
        instance2 = DefrostingProgram()

        self.assertEqual(instance1, instance2)

    def test___init____valid_weight__calculates_cycles_correctly(self):
        self.mock_sensors.inner_weight.return_value = TURNTABLE_WEIGHT_IN_GRAMS + 500
        self.program.sensors = self.mock_sensors
        self.program.__init__()

        self.assertEqual(self.program.cycles, 5)

    def test_control_components__inner_temp_above_target_and_not_just_updated__reduces_cycles(self):
        self.mock_sensors.inner_temp1.return_value = PROGRAM_DEFROSTING_TARGET_TEMP + 1
        self.mock_sensors.inner_temp2.return_value = PROGRAM_DEFROSTING_TARGET_TEMP + 1
        self.program.just_updated = False
        self.program.cycles = 3

        self.program.control_components()

        self.assertEqual(self.program.cycles, 2)

    def test_control_components__inner_temp_below_ambient_plus_5_and_just_updated__resets_just_updated(self):
        self.program.just_updated = True

        self.program.control_components()

        self.assertFalse(self.program.just_updated)

    def test_control_components__cycles_zero_or_less__sets_finished_to_true(self):
        self.program.cycles = 0

        self.program.control_components()

        self.assertTrue(self.program.finished)

    def test_control_components__too_many_cycles__sets_magnetron_power_share_correctly(self):
        self.mock_sensors.inner_temp1.return_value = 20
        self.mock_sensors.inner_temp2.return_value = 20
        self.program.just_updated = False
        self.program.cycles = 5

        self.program.control_components()

        self.mock_magnetron.set_target_power_share.assert_called_with(0.4)

    def test_control_components__valid_cycles__sets_magnetron_power_share_correctly(self):
        self.mock_sensors.inner_temp1.return_value = 20
        self.mock_sensors.inner_temp2.return_value = 20
        self.program.just_updated = False
        self.program.cycles = 1

        self.program.control_components()

        self.mock_magnetron.set_target_power_share.assert_called_with(0.2)
