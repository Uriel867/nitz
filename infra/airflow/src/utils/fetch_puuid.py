from .http_requests import request_with_handle
import os
import logging

logger = logging.getLogger(__name__)

async def fetch_puuid(tag_line: str, summoner_name: str, region: str):
    logger.info(f'Fetching puuid for summoner: {summoner_name} with tag: {tag_line}')
    summoner_data = await request_with_handle(method='GET', url=f'{os.getenv("NITZ_API_URL")}/account/by-id/{region}/{summoner_name}/{tag_line}')
    return summoner_data['puuid']