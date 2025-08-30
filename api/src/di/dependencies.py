from typing import Annotated
from fastapi import Depends, Request
from reporter.service import LoLStatsService
from pymongo import MongoClient
from traffic_managment.riot_limiter import RiotLimiter
import asyncio

account_puuid_limiter = RiotLimiter(capacity=1000,leak_rate=1000/60)

def provide_mongo_client():
    mongo_client = MongoClient(host="mongodb")
    
    yield mongo_client
    
# Dependency function for LoLStatsService
def get_lol_stats_service(
    mongo_client: Annotated[MongoClient, Depends(provide_mongo_client)]
) -> LoLStatsService:
    return LoLStatsService(mongo_client)

async def acquire_account_puuid_limiter(request: Request):
    print(f'Bucket level is: {account_puuid_limiter.bucket.level}')
    await account_puuid_limiter.acquire()
    

