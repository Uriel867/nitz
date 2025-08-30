import os
from fastapi import APIRouter, Depends
import requests
from  di.dependencies import acquire_account_puuid_limiter

router = APIRouter()

@router.get("/account/{region}/{game_name}/{tag_line}", dependencies=[Depends(acquire_account_puuid_limiter)])
def get_account_puuid(tag_line: str,
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