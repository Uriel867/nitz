import os
from fastapi import APIRouter, Depends
import requests
from  di.dependencies import acquire_account_puuid_limiter,acquire_account_by_id_limiter,acquire_match_by_match_id_limiter

router = APIRouter()

@router.get("/account/{region}/{game_name}/{tag_line}", dependencies=[Depends(acquire_account_by_id_limiter)])
def get_account_by_id(tag_line: str,
                game_name: str,
                region: str='europe'
):
    url = f'https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}'
    headers = {
        "X-Riot-Token": os.getenv("RIOT_API_KEY")
    }
    
    response = requests.get(url,headers=headers)
    if "status" in response.json().keys():
        return {"success":False}
    return response.json()

@router.get("/account/{region}/{puuid}",dependencies=[Depends(acquire_account_puuid_limiter)])
def get_account_by_puuid(puuid: str,
                         region: str='europe'
):
    url = f'https://{region}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}'
    headers = {
        "X-Riot-Token": os.getenv("RIOT_API_KEY")
    }
    response = requests.get(url,headers=headers)
    if "status" in response.json().keys():
        return {"success":False}
    return response.json()

@router.get("/match/{match_id}",dependencies=[Depends(acquire_match_by_match_id_limiter)])
def get_match_by_match_id(
    match_id: str,
    region: str='europe'
):
    url = f'https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}'
    headers = {
        "X-Riot-Token": os.getenv("RIOT_API_KEY")
    }
    response = requests.get(url,headers=headers)
    if "status" in response.json().keys():
        return {"success":False}
    return response.json()