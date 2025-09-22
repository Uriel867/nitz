from typing import Annotated
from fastapi import Depends, Request
from reporter.service import LoLStatsService
from pymongo import MongoClient
from traffic_managment.async_leaky_bucket import AsyncLeakyBucket
from riot_games.service import RiotGamesService
import os
from sqlalchemy import create_engine, MetaData
from reporter.service import LoLStatsService
from scraper.service import ScraperService

#Buckets
api_key_small_limiter = AsyncLeakyBucket(capacity=20, leak_rate=20/1) # 20 requests every 1 second
api_key_big_limiter = AsyncLeakyBucket(capacity=100, leak_rate=100/120) # 100 requests every 2 minutes
account_by_id_limiter = AsyncLeakyBucket(capacity=1000, leak_rate=1000/60) # 2000 requests every 1 minute
account_by_puuid_limiter = AsyncLeakyBucket(capacity=1000, leak_rate=1000/60) # 1000 requests every 1 minute
match_by_match_id_limiter = AsyncLeakyBucket(capacity=2000, leak_rate=2000/10) # 2000 requests every 10 seconds
match_timeline_by_match_id_limiter = AsyncLeakyBucket(capacity=2000, leak_rate=2000/10) # 2000 requests every 10 seconds
matches_by_puuid_limiter = AsyncLeakyBucket(capacity=2000, leak_rate=2000/10) # 2000 requests every 10 seconds

riot_games_service = RiotGamesService(os.getenv("RIOT_API_KEY"))

_postgres_engine = None
_postgres_metadata = None

#Dependencies for LolStatsService
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

#Dependency for RiotGames
async def acquire_api_key_small_limiter():
    await api_key_small_limiter.acquire()

async def acquire_api_key_big_limiter():
    await api_key_big_limiter.acquire()

async def acquire_account_puuid_limiter(request: Request):
    await account_by_puuid_limiter.acquire()
    
async def acquire_account_by_id_limiter(request: Request):
    await account_by_id_limiter.acquire()
    
async def acquire_match_by_match_id_limiter(request: Request):
    await match_by_match_id_limiter.acquire()
    
async def acquire_match_timeline_by_match_id_limiter(request: Request):
    await match_timeline_by_match_id_limiter.acquire()

async def acquire_matches_by_puuid_limiter(request: Request):
    await matches_by_puuid_limiter.acquire()

# scraper dependencies
def provide_scraper_service():
    scraper_service = ScraperService()

    yield scraper_service
    # anything that needs to be executed after the function that's being injected with this dependency should go here
    # for example, closing a db connection

# postgres
def provide_postgres_metadata():
    global _postgres_metadata
    if not _postgres_metadata:
        _postgres_metadata = MetaData()
    return _postgres_metadata

def provide_postgres_engine():
    global _postgres_engine
    if not _postgres_engine:
        _postgres_engine = create_engine(os.environ['POSTGRES_DB_URL'], echo=True)
    
    yield _postgres_engine

