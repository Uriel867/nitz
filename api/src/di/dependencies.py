from typing import Annotated
from fastapi import Depends, Request
from reporter.service import LoLStatsService
from pymongo import MongoClient
from traffic_managment.async_leaky_bucket import AsyncLeakyBucket
from riot_games.service import RiotGamesService
import os
from sqlalchemy import create_engine, MetaData
from reporter.service import LoLStatsService
from scraper.service import LeagueOfGraphsScraperService

#Buckets
account_by_id_limiter = AsyncLeakyBucket(capacity=1000,leak_rate=1000/60) # 2000 requests every 1 minute
account_by_puuid_limiter = AsyncLeakyBucket(capacity=1000,leak_rate=1000/60) # 1000 requests every 1 minute
match_by_id_limiter = AsyncLeakyBucket(2000,2000/10) # 2000 requests every 10 seconds

riot_games_service = RiotGamesService(os.getenv("RIOT_API_KEY"))

#Dependencies for LolStatsService
def provide_mongo_client():
    mongo_host = os.getenv("MONGO_HOST")
    mongo_client = MongoClient(host=mongo_host)
    
    try:
        yield mongo_client
    
    finally:
        mongo_client.close()
    
def provide_lol_stats_service(
    mongo_client: Annotated[MongoClient, Depends(provide_mongo_client)]) -> LoLStatsService:
    return LoLStatsService(mongo_client)

#Dependencies for RiotGameService
def provide_riot_games_service():
    yield riot_games_service


#Dependency for RiotGames
async def acquire_account_puuid_limiter(request: Request):
    await account_by_puuid_limiter.acquire()
    
async def acquire_account_by_id_limiter(request: Request):
    await account_by_id_limiter.acquire()
    
async def acquire_match_by_match_id_limiter(request: Request):
    await match_by_id_limiter.acquire()

def provide_scraper():
    scraper = LeagueOfGraphsScraperService()
    
scraper_service = None
_postgres_engine = None
_postgres_metadata = None

def provide_scraper_service():
    scraper_service = LeagueOfGraphsScraperService()

    yield scraper_service
    # anything that needs to be executed after the function that's being injected with this dependency should go here
    # for example, closing a db connection

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

def provide_mongo_client():
    mongo_client = MongoClient(host="mongodb")
    
    yield mongo_client
    
# Dependency function for LoLStatsService
def provide_lol_stats_service(
    mongo_client: Annotated[MongoClient, Depends(provide_mongo_client)]
) -> LoLStatsService:
    return LoLStatsService(mongo_client)
