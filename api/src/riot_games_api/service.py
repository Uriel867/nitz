import os
import requests

def get_account_by_id(tag_line: str, game_name: str, region: str='europe'):
    url = f'https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}'
    headers = {
        "X-Riot-Token": os.getenv("RIOT_API_KEY")
    }
    
    response = requests.get(url,headers=headers)
    if "status" in response.json().keys():
        return {"success":False}
    return response.json()

def get_account_by_puuid(puuid: str, region: str='europe'):
    url = f'https://{region}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}'
    headers = {
        "X-Riot-Token": os.getenv("RIOT_API_KEY")
    }
    response = requests.get(url,headers=headers)
    if "status" in response.json().keys():
        return {"success":False}
    return response.json()

def get_match_by_match_id(match_id: str, region: str='europe'):
    url = f'https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}'
    headers = {
        "X-Riot-Token": os.getenv("RIOT_API_KEY")
    }
    response = requests.get(url,headers=headers)
    if "status" in response.json().keys():
        return {"success":False}
    return response.json()