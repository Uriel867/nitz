from typing import Annotated
from fastapi import Depends
from pymongo import MongoClient
import os
from sqlalchemy import create_engine, MetaData

from reporter.service import LoLStatsService
from scraper.service import LeagueOfGraphsScraperService


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
    mongo_client = MongoClient(host=os.environ['MONGODB_URL'], port=int(os.environ['MONGODB_PORT']))
    
    yield mongo_client
    
# Dependency function for LoLStatsService
def provide_lol_stats_service(
    mongo_client: Annotated[MongoClient, Depends(provide_mongo_client)]
) -> LoLStatsService:
    return LoLStatsService(mongo_client)
