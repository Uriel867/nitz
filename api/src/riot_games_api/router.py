from fastapi import APIRouter, Depends
from  di.dependencies import acquire_account_puuid_limiter,acquire_account_by_id_limiter,acquire_match_by_match_id_limiter
from riot_games_api.service import get_account_by_id as service_get_account_by_id
from riot_games_api.service import get_account_by_puuid as service_get_account_by_puuid
from riot_games_api.service import get_match_by_match_id as service_get_match_by_match_id
router = APIRouter()

@router.get("/account/{region}/{game_name}/{tag_line}", dependencies=[Depends(acquire_account_by_id_limiter)])
def get_account_by_id(tag_line: str,
                game_name: str,
                region: str='europe'
):
    return service_get_account_by_id(tag_line=tag_line, game_name=game_name,region=region)

@router.get("/account/{region}/{puuid}",dependencies=[Depends(acquire_account_puuid_limiter)])
def get_account_by_puuid(puuid: str,
                         region: str='europe'
):
    return service_get_account_by_puuid(puuid=puuid, region=region)

@router.get("/match/{match_id}",dependencies=[Depends(acquire_match_by_match_id_limiter)])
def get_match_by_match_id(
    match_id: str,
    region: str='europe'
):
    return service_get_match_by_match_id(match_id=match_id, region=region)