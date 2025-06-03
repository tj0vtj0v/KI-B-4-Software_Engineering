class Ringbuffer:
    def __init__(self, size):
        self.size = size
        self.buffer = [None] * size
        self.index = 0

    def add(self, item):
        self.buffer[self.index] = item
        self.index = (self.index + 1) % self.size

    def get(self):
        return [item for item in (self.buffer[self.index:] + self.buffer[:self.index]) if item is not None]

    def __len__(self):
        return len(self.get())
