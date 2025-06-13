class Ringbuffer:
    """
    A fixed-size ring buffer (circular buffer) for storing items in a FIFO manner.

    :param size: The maximum number of items the buffer can hold.
    :type size: int
    :raises ValueError: If the provided size is not a positive integer.
    """

    def __init__(self, size: int) -> None:
        """
        Initialize the ring buffer with a given size.

        :param size: The maximum number of items the buffer can hold.
        :type size: int
        :raises ValueError: If size is not a positive integer.
        """
        if size <= 0:
            raise ValueError("Size must be a positive integer")

        self.size: int = size
        self.buffer: list = [None] * size
        self.index: int = 0

    def add(self, item: object) -> None:
        """
        Add an item to the buffer at the current index. Overwrites the oldest item if the buffer is full.

        :param item: The item to add to the buffer. If None, the buffer is not updated.
        :type item: object
        :return: None
        """
        if item is not None:
            self.buffer[self.index] = item
            self.index = (self.index + 1) % self.size

    def get(self) -> list:
        """
        Retrieve the items in the buffer in the correct order, omitting None values.

        :return: A list of items currently in the buffer, in FIFO order.
        :rtype: list
        """
        return [item for item in (self.buffer[self.index:] + self.buffer[:self.index]) if item is not None]

    def __len__(self) -> int:
        """
        Get the number of non-None items currently stored in the buffer.

        :return: The number of valid items in the buffer.
        :rtype: int
        """
        return len(self.get())
