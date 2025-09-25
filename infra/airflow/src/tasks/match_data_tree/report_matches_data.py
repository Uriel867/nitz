from airflow.operators.python import get_current_context
from utils.http_requests import request_with_handle
import os
import asyncio

def fetch_and_report_all_matches_task():
    current_task = get_current_context()['ti']
    matches_ids = current_task.xcom_pull(task_ids='match_tree')
    asyncio.run(fetch_and_report_all_matches(matches_ids))

async def fetch_and_report_all_matches(matches_ids):
    fetch_and_report = [fetch_and_report_match(match_id) for match_id in matches_ids]
    await asyncio.gather(*fetch_and_report)

#iterate through the list of matches and report each one
async def fetch_and_report_match(match_id):
    match_data = await fetch_match_data(match_id)
    await report_match(match_id, match_data)


async def fetch_match_data(match_id: str):
    return await request_with_handle('GET',f'{os.getenv('NITZ_API_URL')}/match/by-match-id/{match_id}')


async def report_match(match_id:str, match_data: dict):
    await request_with_handle(method='POST', url=f'{os.getenv('NITZ_API_URL')}/reporter/match', params={'match_id': match_id}, json=match_data )
