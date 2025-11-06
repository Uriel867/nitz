from typing import Annotated
from fastapi import APIRouter, Depends
from di.dependencies import  provide_riot_games_service
from riot_games.service import RiotGamesService
from riot_games.models import RiotGamesRegion

router = APIRouter()

RiotGamesServiceDependency = Annotated[RiotGamesService, Depends(provide_riot_games_service)]

@router.get("/account/by-id/{region}/{game_name}/{tag_line}")
def get_account_by_riot_id(tag_line: str,
                game_name: str,
                service: RiotGamesServiceDependency,
                region: RiotGamesRegion=RiotGamesRegion.EUROPE
):
    return service.get_account_by_riot_id(tag_line=tag_line, game_name=game_name, region=region)

@router.get("/account/by-puuid/{region}/{puuid}")
def get_account_by_puuid(puuid: str,
                         service: RiotGamesServiceDependency,
                         region: RiotGamesRegion=RiotGamesRegion.EUROPE
):
    return service.get_account_by_puuid(puuid=puuid, region=region)

@router.get("/match/by-match-id/{match_id}")
def get_match_by_match_id(
    match_id: str,
    service: RiotGamesServiceDependency,
    region: RiotGamesRegion=RiotGamesRegion.EUROPE
):
    return service.get_match_by_match_id(match_id=match_id, region=region)

@router.get("/match/by-puuid/{puuid}")
def get_matches_by_puuid(
    puuid: str,
    service: RiotGamesServiceDependency,
    region: RiotGamesRegion=RiotGamesRegion.EUROPE
):
    return service.get_matches_by_puuid(puuid=puuid, region=region)

@router.get("/match/timeline/by-match-id/{match_id}")
def get_match_timeline_by_match_id(
    match_id: str,
    service: RiotGamesServiceDependency,
    region: RiotGamesRegion=RiotGamesRegion.EUROPE
):
    return service.get_match_timeline_by_match_id(match_id=match_id, region=region)
