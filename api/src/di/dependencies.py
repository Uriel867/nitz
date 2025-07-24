from typing import Annotated
from fastapi import Depends
from pymongo import MongoClient
import os
from sqlalchemy import create_engine

from reporter.service import LoLStatsService
from scraper.service import LeagueOfGraphsScraperService


def provide_mongo_client():
    mongo_client = MongoClient(host="mongodb")
    
    yield mongo_client
    
# Dependency function for LoLStatsService
def get_lol_stats_service(
    mongo_client: Annotated[MongoClient, Depends(provide_mongo_client)]
) -> LoLStatsService:
    return LoLStatsService(mongo_client)

engine = None
scraper_service = None

def provide_scraper_service():
    global scraper_service
    if not scraper_service:
        scraper_service = LeagueOfGraphsScraperService()

    yield scraper_service
    # anything that needs to be executed after the function that's being injected with this dependency should go here
    # for example, closing a db connection

def provide_postgres_engine():
    global engine
    if not engine:
        engine = create_engine(os.environ['POSTGRES_DB_URL'], echo=True)
    
    yield engine
