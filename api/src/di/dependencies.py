from typing import Annotated
from fastapi import Depends, Request
from reporter.service import LoLStatsService
from pymongo import MongoClient
from api.src.traffic_managment.async_leaky_bucket import AsyncLeakyBucket
from riot_games.service import RiotGamesService
import asyncio
import os

#Buckets
account_by_id_limiter = AsyncLeakyBucket(capacity=1000,leak_rate=1000/60) # 2000 requests every 1 minute
account_by_puuid_limiter = AsyncLeakyBucket(capacity=1000,leak_rate=1000/60) # 1000 requests every 1 minute
match_by_id_limiter = AsyncLeakyBucket(2000,2000/10) # 2000 requests every 10 seconds

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
    riot_games_service = RiotGamesService(os.getenv("RIOT_API_KEY"))
    
    yield riot_games_service


#Dependency for RiotGames
async def acquire_account_puuid_limiter(request: Request):
    await account_by_puuid_limiter.acquire()
    
async def acquire_account_by_id_limiter(request: Request):
    await account_by_id_limiter.acquire()
    
async def acquire_match_by_match_id_limiter(request: Request):
    await match_by_id_limiter.acquire()


