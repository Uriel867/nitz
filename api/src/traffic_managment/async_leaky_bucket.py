import asyncio
from .leaky_bucket import LeakyBucket

class AsyncLeakyBucket:
    def __init__(self,capacity, leak_rate):
        self.bucket = LeakyBucket(capacity=capacity, leak_rate_per_sec=leak_rate)
        self._lock = asyncio.Lock()  # atomic check+reserve across tasks

    async def acquire(self, amount: float = 1.0):
        while True:
            async with self._lock:
                tta = self.bucket.time_to_allow(amount)
                if tta <= 0:
                    self.bucket.reserve(amount)
                    return
            await asyncio.sleep(tta)
