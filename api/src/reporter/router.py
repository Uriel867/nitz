from fastapi import APIRouter, Depends
from typing import Annotated
from reporter.service import LoLStatsService, get_lol_stats_service

router = APIRouter(prefix="/reporter")
LoLStatsServiceDependency = Annotated[LoLStatsService,Depends(get_lol_stats_service)]

@router.get("/match/{match_id}")
def get_match_id(
    match_id: str,
    service: LoLStatsServiceDependency
):
    """
    Retrieves a match from the MongoDB collection based on match_id.
    
    :param match_id: The ID of the match to retrieve
    :return: The match data or a message if the match is not found
    """
    
    return service.get_match_id(match_id)

@router.post("/match")
def insert_match_id(
    match_id: str,
    service: LoLStatsServiceDependency
):  
    """
    Inserts match id into the MongoDB collection.
    
    :param match_id: Match id to be inserted (received from API request)
    """
    
    return service.insert_match_id(match_id)

@router.get("/by-summoner/{summoner_puuid}")
def get_match_data_by_summoner(
    summoner_puuid: str,
    service: LoLStatsServiceDependency
):
    return service.get_match_data_by_summoner(summoner_puuid)

@router.get("/by-id/{match_id}")
def get_match_data_by_id(
    match_id: str,
    service: LoLStatsServiceDependency
):
    return service.get_match_data_by_id(match_id)

@router.post("/summoner")  
def insert_summoner(
    summoner_name: str,
    puuid: str,
    service: LoLStatsServiceDependency
):
    """
    Inserts summoner data directly into the MongoDB collection.
    
    :param summoner_data: Summoner data to be inserted (received from API request)
    """
    return service.insert_summoner(summoner_name,puuid)

@router.post("/multiple")
def insert_many_summoners(
    summoner_data: List[Dict],
    service: LoLStatsServiceDependency
):
    """
    Inserts multiple summoner data into the MongoDB collection.
    
    :param summoner_data: List of summoner data to be inserted (received from API request)
    """
    return service.insert_many_summoners(summoner_data)

@router.get("/all")
def get_all_summoners(
    service: LoLStatsServiceDependency
):
    """
    Retrieves all summoners from the MongoDB collection.
    
    :return: List of all summoners or a message if no summoners are found
    """
    return service.get_all_summoners()

@router.get("/summoner/{summoner_name}/{puuid}")
def get_summoner(
    summoner_name: str,
    puuid: int,
    service: LoLStatsServiceDependency
):
    """
    Retrieves a summoner from the MongoDB collection based on summoner_name and battle_tag.
    
    :param summoner_name: The name of the summoner to retrieve
    :param battle_tag: The battle tag of the summoner to retrieve
    :return: The summoner data or a message if the summoner is not found
    """
    return service.get_summoner(summoner_name, puuid)