from typing import Annotated
from fastapi import Depends, Request
from reporter.service import LoLStatsService
from pymongo import MongoClient
from traffic_managment.riot_limiter import RiotLimiter
import asyncio

#Buckets
account_by_id_limiter = RiotLimiter(capacity=1000,leak_rate=1000/60)
account_by_puuid_limiter = RiotLimiter(capacity=1000,leak_rate=1000/60)
match_by_id_limiter = RiotLimiter(2000,2000/10)

def provide_mongo_client():
    mongo_client = MongoClient(host="mongodb")
    
    yield mongo_client
    
# Dependency function for LoLStatsService
def get_lol_stats_service(
    mongo_client: Annotated[MongoClient, Depends(provide_mongo_client)]
) -> LoLStatsService:
    return LoLStatsService(mongo_client)


#Dependency for RiotGames
async def acquire_account_puuid_limiter(request: Request):
    await account_by_id_limiter.acquire()
    
async def acquire_account_by_id_limiter(request: Request):
    await account_by_puuid_limiter.acquire()
    
async def acquire_match_by_match_id_limiter(request: Request):
    await match_by_id_limiter.acquire()
    

