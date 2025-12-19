import asyncio
import logging
from typing import List, Union, Dict
from utils.http_requests import request_with_handle

logger = logging.getLogger(__name__)

def fetch_and_report_chunk_task(chunk: List[str], fetch_url: str, report_url: str, summoner: bool, match: bool):
    asyncio.run(fetch_and_report_chunk(chunk, fetch_url, report_url, summoner, match))

async def fetch_and_report_chunk(chunk: List[str], fetch_url: str, report_url: str, summoner: bool, match: bool):
    chunk_data = [fetch_and_report(item, fetch_url, report_url, summoner , match) for item in chunk['data']]

    await asyncio.gather(*chunk_data)

async def fetch_and_report(item: Union[Dict[str, str], str], fetch_url: str, report_url: str, summoner: bool, match: bool):
    data = None
    if summoner:
        game_name = item['game_name']
        tag_line = item['tag_line']
        region = item['region']
        fetch_url += f'/{region}/{game_name}/{tag_line}'
        data = await fetch_data(fetch_url, [game_name, tag_line])
        await report_data('PATCH', report_url, [game_name, tag_line, data], summoner, match)

    if match:
        match_id = item
        fetch_url += f'/{match_id}'
        logger.info(f'url is {fetch_url}')
        data = await fetch_data(fetch_url, [item])
        logger.info(f'data is {data}')
        await report_data('POST', report_url, [item, data], summoner, match)
    logger.info('Fetched data %s', item)

    return data


async def fetch_data(fetch_url: str, data_to_fetch: List[any]):
    logger.info('Fetching data %s', data_to_fetch)
    return await request_with_handle('GET', fetch_url)

async def report_data(method: str, report_url: str, data_to_report: List[any], summoner: bool, match: bool):
    if summoner:
        json = {
            'game_name': data_to_report[0],
            'tag_line': data_to_report[1],
            'puuid': data_to_report[2].get('puuid'),
        }
        return await request_with_handle(method, report_url, json=json)

    if match:
        params = {
            "match_id": data_to_report[0],
        }

        json = data_to_report[1]

        return await request_with_handle(method, report_url, json=json, params=params)
