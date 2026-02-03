import os
from pathlib import Path
from typing import Annotated
from fastapi import Depends
from pymongo import MongoClient
from redis import Redis

from riot_games.service import RiotGamesService
from reporter.service import LoLStatsService
from scraper.service import ScraperService
from rate_limiter.rate_limiter import LeakyBucketRateLimiter


redis_client = Redis(host=os.getenv('REDIS_URL', 'redis'), port=os.getenv('REDIS_PORT', 6379), db=0)

riot_games_service = RiotGamesService(os.getenv('RIOT_API_KEY'))

def provide_redis() -> Redis:
    yield redis_client

def provide_rate_limiter(redis: Annotated[Redis, Depends(provide_redis)]) -> LeakyBucketRateLimiter:
    return LeakyBucketRateLimiter(
        capacity=50,
        leak_rate=50/60,
        max_wait_time=60.0,
        script_path=Path('..') / 'conf' / 'leaky_bucket.lua',
        redis_client=redis
    )

# dependencies for LolStatsService
def provide_mongo_client():
    mongo_host = os.getenv("MONGODB_URL")
    mongo_client = MongoClient(host=mongo_host)
    
    try:
        yield mongo_client
    
    finally:
        mongo_client.close()
    
def provide_lol_stats_service(
    mongo_client: Annotated[MongoClient, Depends(provide_mongo_client)]
) -> LoLStatsService:
    return LoLStatsService(mongo_client)

#Dependencies for RiotGameService
def provide_riot_games_service():
    yield riot_games_service

# scraper dependencies
def provide_scraper_service():
    scraper_service = ScraperService()

    yield scraper_service
    # anything that needs to be executed after the function that's being injected with this dependency should go here
    # for example, closing a db connection
