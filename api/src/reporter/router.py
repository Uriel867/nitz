from fastapi import APIRouter, Depends
from typing import Annotated,List,Dict
from reporter.service import LoLStatsService
from di.dependencies import get_lol_stats_service
from .models import SummonerModel

router = APIRouter(prefix="/reporter")
LoLStatsServiceDependency = Annotated[LoLStatsService,Depends(get_lol_stats_service)]


@router.get("/by-id/{match_id}")
def get_match_data_by_id(
    match_id: str,
    service: LoLStatsServiceDependency
):
    return service.get_match_data_by_id(match_id=match_id)

@router.post("/match")
def insert_match_data_by_id(
    match_id: str,
    match_data: Dict,
    service: LoLStatsServiceDependency
):
    
    return service.insert_match_data_by_id(match_id=match_id, match_data=match_data)


@router.post("/summoner")  
def insert_summoner(
    model: SummonerModel,
    service: LoLStatsServiceDependency
):
    """
    Inserts summoner data directly into the MongoDB collection.
    
    :param summoner_data: Summoner data to be inserted (received from API request)
    """
    return service.insert_summoner(summoner_name=model.summoner_name, tag_line=model.tag_line)

@router.post("/multiple")
def insert_many_summoners(
    summoner_list: List[Dict],
    service: LoLStatsServiceDependency
):
    """
    Inserts multiple summoner data into the MongoDB collection.
    
    :param summoner_data: List of summoner data to be inserted (received from API request)
    """
    return service.insert_many_summoners(summoners_list=summoner_list)

@router.get("/all")
def get_all_summoners(
    service: LoLStatsServiceDependency
):
    """
    Retrieves all summoners from the MongoDB collection.
    
    :return: List of all summoners or a message if no summoners are found
    """
    return service.get_all_summoners()
