import unittest

from src.helper.Ringbuffer import Ringbuffer


class TestRingbuffer(unittest.TestCase):
    def test_add__full_buffer__returns_all_elements(self):
        rb = Ringbuffer(3)

        rb.add(1)
        rb.add(2)
        rb.add(3)
        self.assertEqual(rb.get(), [1, 2, 3])

    def test_add__overwrite_oldest__returns_new_elements(self):
        rb = Ringbuffer(3)

        rb.add(1)
        rb.add(2)
        rb.add(3)
        rb.add(4)
        self.assertEqual(rb.get(), [2, 3, 4])

    def test_add__partial_fill__returns_partial_elements(self):
        rb = Ringbuffer(3)

        rb.add(1)
        rb.add(2)
        self.assertEqual(rb.get(), [1, 2])

    def test_len__various_operations__returns_correct_length(self):
        rb = Ringbuffer(3)
        self.assertEqual(len(rb), 0)

        rb.add(1)
        self.assertEqual(len(rb), 1)

        rb.add(2)
        rb.add(3)
        self.assertEqual(len(rb), 3)

        rb.add(4)
        self.assertEqual(len(rb), 3)

    def test_get__empty_buffer__returns_empty_list(self):
        rb = Ringbuffer(3)
        self.assertEqual(rb.get(), [])

    def test_get__partially_filled_buffer__returns_correct_elements(self):
        rb = Ringbuffer(5)

        rb.add(10)
        rb.add(20)
        self.assertEqual(rb.get(), [10, 20])

    def test_add__non_integer_elements__stores_and_returns_correctly(self):
        rb = Ringbuffer(3)

        rb.add("a")
        rb.add("b")
        rb.add("c")
        self.assertEqual(rb.get(), ["a", "b", "c"])

    def test_add__overwrite_with_mixed_types__returns_correct_elements(self):
        rb = Ringbuffer(3)

        rb.add(1)
        rb.add("b")
        rb.add(3.5)
        rb.add(True)
        self.assertEqual(rb.get(), ["b", 3.5, True])

    def test_len__empty_buffer__returns_zero(self):
        rb = Ringbuffer(3)
        self.assertEqual(len(rb), 0)

    def test_len__after_overwrite__returns_correct_length(self):
        rb = Ringbuffer(2)

        rb.add(1)
        rb.add(2)
        rb.add(3)
        self.assertEqual(len(rb), 2)
