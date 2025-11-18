import os
import asyncio
import logging
from typing import List
from utils.http_requests import request_with_handle

logger = logging.getLogger(__name__)

#iterate through the list of matches and report each one
async def fetch_and_report_match(match_id: str):
    logger.info('Fetching match %s', match_id)
    match_data = await fetch_match_data(match_id)
    logger.info('Fetched match %s', match_id)
    await report_match(match_id, match_data)

def fetch_and_report_chunk_task(matches_ids_chunk: List[str]):
    asyncio.run(fetch_and_report_chunk(matches_ids_chunk))

async def fetch_and_report_chunk(matches_ids_chunk: List[str]):
    fetch_and_report = [fetch_and_report_match(match_id) for match_id in matches_ids_chunk]
    await asyncio.gather(*fetch_and_report)

async def fetch_match_data(match_id: str):
    return await request_with_handle(method='GET', url=f'{os.getenv("NITZ_API_URL")}/match/by-match-id/{match_id}')


async def report_match(match_id: str, match_data: dict):
    await request_with_handle(method='POST', url=f'{os.getenv("NITZ_API_URL")}/reporter/match', params={'match_id': match_id}, json=match_data )
