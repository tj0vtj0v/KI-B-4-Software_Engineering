class Ringbuffer:
    def __init__(self, size: int):
        if size <= 0:
            raise ValueError("Size must be a positive integer")

        self.size = size
        self.buffer = [None] * size
        self.index = 0

    def add(self, item):
        if item is not None:
            self.buffer[self.index] = item
            self.index = (self.index + 1) % self.size

    def get(self):
        return [item for item in (self.buffer[self.index:] + self.buffer[:self.index]) if item is not None]

    def __len__(self):
        return len(self.get())
