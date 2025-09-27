import time


class LeakyBucket:
    def __init__(self, capacity: float, leak_rate_per_sec: float):
        self.capacity = float(capacity)
        self.leak_rate = float(leak_rate_per_sec)
        self.level = 0.0
        self.last_ts = time.monotonic()

    def _leak(self):
        now = time.monotonic()
        elapsed = now - self.last_ts
        self.last_ts = now
        self.level = max(0.0, self.level - self.leak_rate * elapsed)

    def time_to_allow(self, amount: float = 1.0) -> float:
        self._leak()
        over = self.level + amount - self.capacity
        if over <= 0:
            return 0.0
        if self.leak_rate == 0:
            return float("inf")
        return over / self.leak_rate

    def reserve(self, amount: float = 1.0) -> bool:
        self._leak()
        if self.level + amount <= self.capacity:
            self.level += amount
            return True
        return False
