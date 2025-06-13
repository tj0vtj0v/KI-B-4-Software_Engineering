from src.helper.Ringbuffer import Ringbuffer


class MagnetronRingbuffer(Ringbuffer):
    """
    A specialized ring buffer for storing boolean values, tracking the number of filled slots,
    and providing a method to calculate the share of `True` values (power share).
    """

    def __init__(self, size: int) -> None:
        """
        Initialize the MagnetronRingbuffer with a given size.

        :param size: The maximum number of items the buffer can hold.
        :type size: int
        :return: None
        """
        super().__init__(int(size))
        self.filled: int = 0

    def add(self, item: bool) -> None:
        """
        Add a boolean item to the buffer. Only boolean values are accepted.

        :param item: The boolean value to add to the buffer.
        :type item: bool
        :raises ValueError: If the item is not a boolean.
        :return: None
        """
        if not isinstance(item, bool):
            raise ValueError("Item must be a boolean value")
        super().add(item)
        self.filled += 1 if self.filled < self.size else 0

    def get(self) -> list:
        """
        Retrieve the contents of the buffer.

        :return: A list containing the buffer's items.
        :rtype: list
        """
        return super().get()

    def power_share(self) -> float:
        """
        Calculate the share of `True` values in the buffer.

        :return: The ratio of `True` values to the number of filled slots, or 0 if empty.
        :rtype: float
        """
        if self.filled == 0:
            return 0
        return sum(self.get()) / self.filled

    def __len__(self) -> int:
        """
        Get the number of items currently in the buffer.

        :return: The number of items in the buffer.
        :rtype: int
        """
        return super().__len__()
