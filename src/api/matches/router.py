from fastapi import APIRouter, Depends
from typing import Annotated
from api.service import MongoService, get_mongo_service

router = APIRouter(prefix="/match")
mongo_service_dependency = Annotated[MongoService,Depends(get_mongo_service)]

@router.get("/match_id/{match_id}")
def get_match_id(
    match_id: str,
    mongo_service: mongo_service_dependency
):
    """
    Retrieves a match from the MongoDB collection based on match_id.
    
    :param match_id: The ID of the match to retrieve
    :return: The match data or a message if the match is not found
    """
    
    return mongo_service.get_match_id(match_id)

@router.post("/insert/match_id/{match_id}")
def insert_match_id(
    match_id: dict,
    mongo_service: mongo_service_dependency
):  
    """
    Inserts match data into the MongoDB collection.
    
    :param match_id: Match data to be inserted (received from API request)
    """
    
    return mongo_service.insert_match_id(match_id)

@router.get("/match_data_by_summoner/{summoner_puuid}")
def get_match_data_by_summoner(
    summoner_puuid: str,
    mongo_service: mongo_service_dependency
):
    return mongo_service.get_match_data_by_summoner(summoner_puuid)

@router.get("/data_by_id/{match_id}")
def get_match_data_by_id(
    match_id: str,
    mongo_service: mongo_service_dependency
):
    return mongo_service.get_match_data_by_id(match_id)