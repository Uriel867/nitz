import os
import requests


class RiotGamesService():
    def __init__(self,api_key: str):
        self.api_key = api_key
       

    def get_account_by_id(self, tag_line: str, game_name: str, region: str='europe'):
        url = f'https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}'
        headers = {
            "X-Riot-Token": self.api_key
        }
        
        response = requests.get(url,headers=headers)
        if "status" in response.json().keys():
            return {"success":False}
        return response.json()

    def get_account_by_puuid(self, puuid: str, region: str='europe'):
        url = f'https://{region}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}'
        headers = {
            "X-Riot-Token": self.api_key
        }
        response = requests.get(url,headers=headers)
        if "status" in response.json().keys():
            return {"success":False}
        return response.json()

    def get_match_by_match_id(self, match_id: str, region: str='europe'):
        url = f'https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}'
        headers = {
            "X-Riot-Token": self.api_key
        }
        response = requests.get(url,headers=headers)
        if "status" in response.json().keys():
            return {"success":False}
        return response.json()