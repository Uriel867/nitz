from redis import Redis
from pathlib import Path

class LeakyBucketRateLimiter:
    def __init__(
        self, 
        capacity: int, 
        leak_rate: float, 
        max_wait_time: float, 
        script_path: Path,
        redis_client: Redis
    ):
        self.capacity = capacity
        self.leak_rate = leak_rate
        self.max_wait_time = max_wait_time
        self.redis_client = redis_client
        self.script_path = script_path

        self.rate_limiter = self._load_leaky_bucket_to_db()

    def _load_leaky_bucket_to_db(self):
        try:
            if self.script_path.exists():
                with open(self.script_path, 'r') as file:
                    script_content = file.read()
                    return self.redis_client.register_script(script_content)
        except Exception as e:
            print(f"Error loading rate limiter script: {e}")
            return None


    async def is_allowed(self, key: str) -> bool:
        if self.rate_limiter is None:
            self._load_leaky_bucket_to_db()

        bucket_key = f'rate_limiter:{key}'

        allowed, queued, wait_time, remaining_tokens = self.rate_limiter(
            keys=[bucket_key],
            args=[self.leak_rate, self.capacity, self.max_wait_time]
        )

        return bool(allowed), bool(queued), float(wait_time), remaining_tokens
