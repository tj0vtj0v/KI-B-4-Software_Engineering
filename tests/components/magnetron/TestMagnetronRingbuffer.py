import unittest
from unittest.mock import MagicMock

from src.components.magnetron.MagnetronRingbuffer import MagnetronRingbuffer


class TestMagnetronRingbuffer(unittest.TestCase):
    def setUp(self):
        self.ringbuffer = MagnetronRingbuffer(5)

    def tearDown(self):
        del self.ringbuffer

    def test_add__valid_boolean__updates_filled_and_length(self):
        self.ringbuffer.add(True)

        self.assertEqual(len(self.ringbuffer), 1)
        self.assertEqual(self.ringbuffer.filled, 1)

    def test_add__invalid_type__raises_value_error(self):
        with self.assertRaises(ValueError):
            self.ringbuffer.add(123)

    def test_add__non_boolean_item__raises_value_error(self):
        with self.assertRaises(ValueError):
            self.ringbuffer.add("string")

    def test_get__empty_buffer__returns_empty_list(self):
        self.assertEqual(self.ringbuffer.get(), [])

    def test_len__empty_buffer__returns_zero(self):
        self.assertEqual(len(self.ringbuffer), 0)

    def test_get__after_adding_items__returns_correct_items(self):
        self.ringbuffer.add(True)
        self.ringbuffer.add(False)

        self.assertEqual(self.ringbuffer.get(), [True, False])

    def test_power_share__empty_buffer__returns_zero(self):
        self.assertEqual(self.ringbuffer.power_share(), 0)

    def test_power_share__non_empty_buffer__returns_correct_ratio(self):
        self.ringbuffer.add(True)
        self.ringbuffer.add(False)
        self.ringbuffer.add(True)

        self.assertEqual(self.ringbuffer.power_share(), 2 / 3)

    def test_len__after_adding_items__returns_correct_length(self):
        self.ringbuffer.add(True)
        self.ringbuffer.add(False)

        self.assertEqual(len(self.ringbuffer), 2)

    def test_add__exceeding_size__overwrites_oldest_item(self):
        self.ringbuffer.add(True)
        self.ringbuffer.add(False)
        self.ringbuffer.add(True)
        self.ringbuffer.add(False)
        self.ringbuffer.add(True)
        self.ringbuffer.add(False)

        self.assertEqual(self.ringbuffer.get(), [False, True, False, True, False])

    def test_power_share__after_overwriting_items__returns_correct_ratio(self):
        self.ringbuffer.add(True)
        self.ringbuffer.add(True)
        self.ringbuffer.add(True)
        self.ringbuffer.add(False)
        self.ringbuffer.add(False)
        self.ringbuffer.add(False)

        self.assertEqual(self.ringbuffer.power_share(), 2 / 5)

    def test_add__boundary_condition_size_one__handles_correctly(self):
        ringbuffer = MagnetronRingbuffer(1)
        ringbuffer.add(True)
        ringbuffer.add(False)

        self.assertEqual(ringbuffer.get(), [False])

    def test_power_share__all_false_items__returns_zero(self):
        self.ringbuffer.add(False)
        self.ringbuffer.add(False)
        self.ringbuffer.add(False)

        self.assertEqual(self.ringbuffer.power_share(), 0)

    def test_power_share__all_true_items__returns_one(self):
        self.ringbuffer.add(True)
        self.ringbuffer.add(True)
        self.ringbuffer.add(True)

        self.assertEqual(self.ringbuffer.power_share(), 1)

    def test_get__mocked_super_get__returns_mocked_value(self):
        self.ringbuffer.get = MagicMock(return_value=[True, False, True])

        self.assertEqual(self.ringbuffer.get(), [True, False, True])
