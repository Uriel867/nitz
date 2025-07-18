from typing import Annotated, List, Dict
from fastapi import APIRouter, Depends
from api.service import LoLStatsService, get_mongo_service

router = APIRouter(prefix="/summoners")
mongo_service_dependency = Annotated[LoLStatsService,Depends(get_mongo_service)]

@router.post("/summoner")  
def insert_summoner(
    summoner_name: str,
    puuid: str,
    mongo_service: mongo_service_dependency
):
    """
    Inserts summoner data directly into the MongoDB collection.
    
    :param summoner_data: Summoner data to be inserted (received from API request)
    """
    return mongo_service.insert_summoner(summoner_name,puuid)

@router.post("/multiple")
def insert_many_summoners(
    summoner_data: List[Dict],
    mongo_service: mongo_service_dependency
):
    """
    Inserts multiple summoner data into the MongoDB collection.
    
    :param summoner_data: List of summoner data to be inserted (received from API request)
    """
    return mongo_service.insert_many_summoners(summoner_data)

@router.get("/all")
def get_all_summoners(
    mongo_service: mongo_service_dependency
):
    """
    Retrieves all summoners from the MongoDB collection.
    
    :return: List of all summoners or a message if no summoners are found
    """
    return mongo_service.get_all_summoners()

@router.get("/summoner/{summoner_name}/{puuid}")
def get_summoner(
    summoner_name: str,
    puuid: int,
    mongo_service: mongo_service_dependency
):
    """
    Retrieves a summoner from the MongoDB collection based on summoner_name and battle_tag.
    
    :param summoner_name: The name of the summoner to retrieve
    :param battle_tag: The battle tag of the summoner to retrieve
    :return: The summoner data or a message if the summoner is not found
    """
    return mongo_service.get_summoner(summoner_name, puuid)