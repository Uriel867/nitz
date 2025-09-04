# external imports
from typing import Annotated
from fastapi import Depends, Request
from reporter.service import LoLStatsService
from pymongo import MongoClient
import os
# internal imports
from scraper.service import LeagueOfGraphsScraper
from traffic_managment.async_leaky_bucket import AsyncLeakyBucket
from riot_games.service import RiotGamesService

#Buckets
account_by_id_limiter = AsyncLeakyBucket(capacity=1000,leak_rate=1000/60) # 2000 requests every 1 minute
account_by_puuid_limiter = AsyncLeakyBucket(capacity=1000,leak_rate=1000/60) # 1000 requests every 1 minute
match_by_id_limiter = AsyncLeakyBucket(2000,2000/10) # 2000 requests every 10 seconds

riot_games_service = RiotGamesService(os.getenv("RIOT_GAMES_API_KEY"))

#Dependencies for LolStatsService
def provide_mongo_client():
    mongo_client = MongoClient(host=os.getenv("MONGODB_URL"))
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

def provide_scraper():
    scraper = LeagueOfGraphsScraper()
    yield scraper
    # anything that needs to be executed after the function that's being injected with this dependency should go here
    # for example, closing a db connection

#Dependency for RiotGames
async def acquire_account_puuid_limiter(request: Request):
    await account_by_puuid_limiter.acquire()
    
async def acquire_account_by_id_limiter(request: Request):
    await account_by_id_limiter.acquire()
    
async def acquire_match_by_match_id_limiter(request: Request):
    await match_by_id_limiter.acquire()


