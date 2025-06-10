from src.helper.Ringbuffer import Ringbuffer


class MagnetronRingbuffer(Ringbuffer):
    def __init__(self, size: int):
        super().__init__(int(size))
        self.filled = 0

    def add(self, item):
        if not isinstance(item, bool):
            raise ValueError("Item must be a boolean value")
        super().add(item)
        self.filled += 1 if self.filled < self.size else 0

    def get(self):
        return super().get()

    def power_share(self):
        if self.filled == 0:
            return 0

        return sum(self.get()) / self.filled

    def __len__(self):
        return super().__len__()
