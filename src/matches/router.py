from fastapi import APIRouter
from src.mongo.service import MongoService

router = APIRouter(prefix="/match")
ms = MongoService()

@router.get("/match_id/{match_id}")
def get_match_id(match_id: str):
    """
    Retrieves a match from the MongoDB collection based on match_id.
    
    :param match_id: The ID of the match to retrieve
    :return: The match data or a message if the match is not found
    """
    
    return ms.get_match_id(match_id)

@router.post("/insert/match_id/{match_id}")
def insert_match_id(match_id: dict):  
    """
    Inserts match data into the MongoDB collection.
    
    :param match_data: Match data to be inserted (received from API request)
    """
    
    return ms.insert_match_id(match_id)

@router.get("/match_data_by_summoner/{summoner_puuid}")
def get_match_data_by_summoner(self, summoner_puuid: str):
    return ms.get_match_data_by_summoner(summoner_puuid)

@router.get("/data_by_id/{match_id}")
def get_match_data_by_id(self,match_id):
    return ms.get_match_data_by_match_id(match_id)