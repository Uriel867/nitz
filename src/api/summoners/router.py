from typing import Annotated, List, Dict
from fastapi import APIRouter, Depends
from api.service import MongoService, get_mongo_service

router = APIRouter(prefix="/summoners")

@router.post("/insert")  
def insert_summoner(
    summoner_data: dict,
    mongo_service: Annotated[MongoService, Depends(get_mongo_service)]
):
    """
    Inserts summoner data directly into the MongoDB collection.
    
    :param summoner_data: Summoner data to be inserted (received from API request)
    """
    return mongo_service.insert_summoner(summoner_data)

@router.post("/insert_many")
def insert_many_summoners(
    summoner_data: List[Dict],
    mongo_service: Annotated[MongoService, Depends(get_mongo_service)]
):
    """
    Inserts multiple summoner data into the MongoDB collection.
    
    :param summoner_data: List of summoner data to be inserted (received from API request)
    """
    return mongo_service.insert_many_summoners(summoner_data)

@router.get("/all")
def get_all_summoners(
    mongo_service: Annotated[MongoService, Depends(get_mongo_service)]
):
    """
    Retrieves all summoners from the MongoDB collection.
    
    :return: List of all summoners or a message if no summoners are found
    """
    return mongo_service.get_all_summoners()

@router.get("/get")
def get_summoner(
    summoner_name: str,
    battle_tag: int,
    mongo_service: Annotated[MongoService, Depends(get_mongo_service)]
):
    """
    Retrieves a summoner from the MongoDB collection based on summoner_name and battle_tag.
    
    :param summoner_name: The name of the summoner to retrieve
    :param battle_tag: The battle tag of the summoner to retrieve
    :return: The summoner data or a message if the summoner is not found
    """
    return mongo_service.get_summoner(summoner_name, battle_tag)