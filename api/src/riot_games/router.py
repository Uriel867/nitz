from typing import Annotated
from fastapi import APIRouter, Depends
from di.dependencies import provide_riot_games_service
from riot_games.service import RiotGamesService
from  di.dependencies import acquire_account_puuid_limiter,acquire_account_by_id_limiter,acquire_match_by_match_id_limiter


router = APIRouter()

riot_games_service_dependency = Annotated[RiotGamesService,Depends(provide_riot_games_service)]

@router.get("/account/{region}/{game_name}/{tag_line}", dependencies=[Depends(acquire_account_by_id_limiter)])
def get_account_by_id(tag_line: str,
                game_name: str,
                service: riot_games_service_dependency,
                region: str='europe',
):
    return service.get_account_by_id(tag_line=tag_line, game_name=game_name,region=region)

@router.get("/account/{region}/{puuid}",dependencies=[Depends(acquire_account_puuid_limiter)])
def get_account_by_puuid(puuid: str,
                         service: riot_games_service_dependency,
                         region: str='europe'
):
    return service.get_account_by_puuid(puuid=puuid, region=region)

@router.get("/match/{match_id}",dependencies=[Depends(acquire_match_by_match_id_limiter)])
def get_match_by_match_id(
    match_id: str,
    service: riot_games_service_dependency,
    region: str='europe'
):
    return service.get_match_by_match_id(match_id=match_id, region=region)