from typing import Annotated
from fastapi import Depends
from pymongo import MongoClient

from reporter.service import LoLStatsService
from scraper.service import LeagueOfGraphsScraper


def provide_mongo_client():
    mongo_client = MongoClient(host="mongodb")
    
    yield mongo_client
    
# Dependency function for LoLStatsService
def get_lol_stats_service(
    mongo_client: Annotated[MongoClient, Depends(provide_mongo_client)]
) -> LoLStatsService:
    return LoLStatsService(mongo_client)

def provide_scraper():
    scraper = LeagueOfGraphsScraper()

    yield scraper
    # anything that needs to be executed after the function that's being injected with this dependency should go here
    # for example, closing a db connection