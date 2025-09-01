import os
import requests


class RiotGamesService():
    def __init__(self,api_key: str):
        self.api_key = api_key
        self.region_placeholder = '<PLACEHOLDER>'
        self.base_url = f'https://{self.region_placeholder}.api.riotgames.com'
        self.headers = {
            "X-Riot-Token": self.api_key
        }

    def get_account_by_riot_id(self, tag_line: str, game_name: str, region: str='europe'):
        base_url = self.base_url.replace(self.region_placeholder, region)
        url = f'{base_url}/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}'
        
        response = requests.get(url,headers=self.headers)
        if "status" in response.json().keys():
            return {"success":False}
        return response.json()

    def get_account_by_puuid(self, puuid: str, region: str='europe'):
        base_url = self.base_url.replace(self.region_placeholder, region)
        url = f'https://{base_url}/riot/account/v1/accounts/by-puuid/{puuid}'
        
        response = requests.get(url,headers=self.headers)
        if "status" in response.json().keys():
            return {"success":False}
        return response.json()

    def get_match_by_match_id(self, match_id: str, region: str='europe'):
        base_url = self.base_url.replace(self.region_placeholder, region)
        url = f'https://{base_url}/lol/match/v5/matches/{match_id}'
        
        response = requests.get(url,headers=self.headers)
        if "status" in response.json().keys():
            return {"success":False}
        return response.json()