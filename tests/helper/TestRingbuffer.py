import unittest

from src.helper.Ringbuffer import Ringbuffer


class TestRingbuffer(unittest.TestCase):
    def setUp(self):
        self.default_size = 3
        self.ringbuffer = Ringbuffer(self.default_size)

    def tearDown(self):
        del self.ringbuffer

    def test_add__full_buffer__returns_all_elements(self):
        self.ringbuffer.add(1)
        self.ringbuffer.add(2)
        self.ringbuffer.add(3)

        self.assertEqual(self.ringbuffer.get(), [1, 2, 3])

    def test_add__overwrite_oldest__returns_new_elements(self):
        self.ringbuffer.add(1)
        self.ringbuffer.add(2)
        self.ringbuffer.add(3)
        self.ringbuffer.add(4)

        self.assertEqual(self.ringbuffer.get(), [2, 3, 4])

    def test_add__partial_fill__returns_partial_elements(self):
        self.ringbuffer.add(1)
        self.ringbuffer.add(2)

        self.assertEqual(self.ringbuffer.get(), [1, 2])

    def test_len__various_operations__returns_correct_length(self):
        self.assertEqual(len(self.ringbuffer), 0)

        self.ringbuffer.add(1)
        self.assertEqual(len(self.ringbuffer), 1)

        self.ringbuffer.add(2)
        self.ringbuffer.add(3)
        self.assertEqual(len(self.ringbuffer), 3)

        self.ringbuffer.add(4)
        self.assertEqual(len(self.ringbuffer), 3)

    def test_get__empty_buffer__returns_empty_list(self):
        self.assertEqual(self.ringbuffer.get(), [])

    def test_get__partially_filled_buffer__returns_correct_elements(self):
        self.ringbuffer.add(10)
        self.ringbuffer.add(20)

        self.assertEqual(self.ringbuffer.get(), [10, 20])

    def test_add__non_integer_elements__stores_and_returns_correctly(self):
        self.ringbuffer.add("a")
        self.ringbuffer.add("b")
        self.ringbuffer.add("c")

        self.assertEqual(self.ringbuffer.get(), ["a", "b", "c"])

    def test_add__overwrite_with_mixed_types__returns_correct_elements(self):
        self.ringbuffer.add(1)
        self.ringbuffer.add("b")
        self.ringbuffer.add(3.5)
        self.ringbuffer.add(True)

        self.assertEqual(self.ringbuffer.get(), ["b", 3.5, True])

    def test_len__empty_buffer__returns_zero(self):
        self.assertEqual(len(self.ringbuffer), 0)

    def test_len__after_overwrite__returns_correct_length(self):
        small_buffer = Ringbuffer(2)

        small_buffer.add(1)
        small_buffer.add(2)
        small_buffer.add(3)

        self.assertEqual(len(small_buffer), 2)

    def test_add__negative_size__raises_exception(self):
        with self.assertRaises(ValueError):
            Ringbuffer(-1)

    def test_add__zero_size__raises_exception(self):
        with self.assertRaises(ValueError):
            Ringbuffer(0)

    def test_get__buffer_with_none_values__ignores_none(self):
        self.ringbuffer.add(None)
        self.ringbuffer.add(1)
        self.ringbuffer.add(None)

        self.assertEqual(self.ringbuffer.get(), [1])

    def test_add__multiple_data_types__handles_correctly(self):
        test_data = [1, "string", 3.14, True, None]
        for item in test_data:
            self.ringbuffer.add(item)

        self.assertEqual(self.ringbuffer.get(), ["string", 3.14, True])

    def test_len__after_clearing_buffer__returns_zero(self):
        self.ringbuffer.add(1)
        self.ringbuffer.add(2)
        self.ringbuffer.buffer = [None] * self.default_size

        self.assertEqual(len(self.ringbuffer), 0)
