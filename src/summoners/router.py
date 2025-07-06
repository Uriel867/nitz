from fastapi import APIRouter
from src.mongo.service import MongoService


router = APIRouter(prefix="/summoners")
ms = MongoService()

@router.post("/insert")  
def insert_summoner(summoner_data: dict):
    """
    Inserts summoner data directly into the MongoDB collection.
    
    :param summoner_data: Summoner data to be inserted (received from API request)
    """
    
    return ms.insert_summoner(summoner_data)

@router.post("/insert_many")
def insert_many_summoners(summoner_data: List[Dict]):
    """
    Inserts multiple summoner data into the MongoDB collection.
    
    :param summoner_data: List of summoner data to be inserted (received from API request)
    """
    
    return ms.insert_many_summoners(summoner_data)

@router.get("/all")
def get_all_summoners():
    """
    Retrieves all summoners from the MongoDB collection.
    
    :return: List of all summoners or a message if no summoners are found
    """
    
    return ms.get_all_summoners()

@router.get("/get")
def get_summoner(summoner_name: str,battle_tag: int):
    """
    Retrieves a summoner from the MongoDB collection based on summoner_name and battle_tag.
    
    :param summoner_name: The name of the summoner to retrieve
    :param battle_tag: The battle tag of the summoner to retrieve
    :return: The summoner data or a message if the summoner is not found
    """
    return ms.get_summoner(summoner_name, battle_tag)