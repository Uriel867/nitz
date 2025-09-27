from typing import Annotated
from fastapi import APIRouter, Depends
from di.dependencies import (
    provide_riot_games_service,
    acquire_account_puuid_limiter, acquire_account_by_id_limiter,
    acquire_match_by_match_id_limiter, acquire_matches_by_puuid_limiter,
    acquire_match_timeline_by_match_id_limiter,
    acquire_api_key_small_limiter, acquire_api_key_big_limiter
)
from riot_games.service import RiotGamesService
from riot_games.models import RiotGamesRegion

# two buckets to limit the api key it self. 120 requests per 2 minutes and 20 requests per 1 second
router = APIRouter(dependencies=[Depends(acquire_api_key_small_limiter),Depends(acquire_api_key_big_limiter)])

RiotGamesServiceDependency = Annotated[RiotGamesService,Depends(provide_riot_games_service)]

@router.get("/account/{region}/{game_name}/{tag_line}", dependencies=[Depends(acquire_account_by_id_limiter)])
def get_account_by_riot_id(tag_line: str,
                game_name: str,
                service: RiotGamesServiceDependency,
                region: RiotGamesRegion=RiotGamesRegion.EUROPE
):
    return service.get_account_by_riot_id(tag_line=tag_line, game_name=game_name,region=region)

@router.get("/account/{region}/{puuid}",dependencies=[Depends(acquire_account_puuid_limiter)])
def get_account_by_puuid(puuid: str,
                         service: RiotGamesServiceDependency,
                         region: RiotGamesRegion=RiotGamesRegion.EUROPE
):
    return service.get_account_by_puuid(puuid=puuid, region=region)

@router.get("/match/by-match-id/{match_id}",dependencies=[Depends(acquire_match_by_match_id_limiter)])
def get_match_by_match_id(
    match_id: str,
    service: RiotGamesServiceDependency,
    region: RiotGamesRegion=RiotGamesRegion.EUROPE
):
    return service.get_match_by_match_id(match_id=match_id, region=region)

@router.get("/match/by-puuid/{puuid}",dependencies=[Depends(acquire_matches_by_puuid_limiter)])
def get_matches_by_puuid(
    puuid: str,
    service: RiotGamesServiceDependency,
    region: RiotGamesRegion=RiotGamesRegion.EUROPE
):
    return service.get_matches_by_puuid(puuid=puuid, region=region)

@router.get("/match/timeline/by-match-id/{match_id}",dependencies=[Depends(acquire_match_timeline_by_match_id_limiter)])
def get_match_timeline_by_match_id(
    match_id: str,
    service: RiotGamesServiceDependency,
    region: RiotGamesRegion=RiotGamesRegion.EUROPE
):
    return service.get_match_timeline_by_match_id(match_id=match_id,region=region)
