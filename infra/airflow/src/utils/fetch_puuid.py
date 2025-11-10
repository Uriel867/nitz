from .http_requests import request_with_handle
import os

async def fetch_puuid(tag_line: str, summoner_name: str, region: str):
    summoner_data = await request_with_handle(method='GET', url=f'{os.getenv("NITZ_API_URL")}/account/by-id/{region}/{summoner_name}/{tag_line}')
    return summoner_data['puuid']