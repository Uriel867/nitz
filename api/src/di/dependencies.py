from pathlib import Path
from typing import Annotated, Generator
from fastapi import Depends, HTTPException
from pymongo import MongoClient
from redis import Redis

from riot_games.service import RiotGamesService
from reporter.service import LoLStatsService
from scraper.service import ScraperService
from rate_limiter.rate_limiter import LeakyBucketRateLimiter
from .settings import Settings

app_settings = Settings()

redis_client = Redis(host=app_settings.REDIS_URL, port=app_settings.REDIS_PORT, db=0)
rate_limiter = LeakyBucketRateLimiter(
    capacity=50,
    leak_rate=50/60,
    max_wait_time=60.0,
    script_path=Path('..') / 'conf' / 'leaky_bucket.lua',
    redis_client=redis_client
)
riot_games_service = RiotGamesService(app_settings.RIOT_API_KEY)

def provide_redis() -> Generator[Redis]:
    yield redis_client

# dependencies for LolStatsService
def provide_mongo_client() -> Generator[MongoClient]:
    mongo_client = MongoClient(host=app_settings.MONGODB_URL, port=int(app_settings.MONGODB_PORT))
    
    try:
        yield mongo_client
    finally:
        mongo_client.close()
    
def provide_lol_stats_service(mongo_client: Annotated[MongoClient, Depends(provide_mongo_client)]) -> LoLStatsService:
    return LoLStatsService(mongo_client)

# dependencies for RiotGameService
def provide_riot_games_service() -> Generator[RiotGamesService]:
    yield riot_games_service

def check_rate_limit(rate_limiter: Annotated[LeakyBucketRateLimiter, Depends(lambda: rate_limiter)]):
    async def dependency(key: str):
        allowed, _, wait_time, _ = await rate_limiter.is_allowed(key)
        if not allowed:
            raise HTTPException(status_code=429, detail=f'Rate limit exceeded. Try again in {wait_time:.2f} seconds.')
    return dependency

# scraper dependencies
def provide_scraper_service() -> Generator[ScraperService]:
    scraper_service = ScraperService()

    yield scraper_service
    # anything that needs to be executed after the function that's being injected with this dependency should go here
    # for example, closing a db connection
