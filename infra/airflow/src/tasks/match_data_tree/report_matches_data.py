from airflow.operators.python import get_current_context
from utils.exceptions import request_with_handle
import os

#iterate through the list of matches and report each one
async def report_matches_to_mongo():
    current_task = get_current_context()['ti']
    matches_ids = current_task.xcom_pull(task_ids='match_tree')

    for match_id in matches_ids:
        match_data = await get_match_data(match_id)
        await report_match(match_id, match_data)


async def get_match_data(match_id: str):
    return request_with_handle('GET',f'{os.getenv('NITZ_API_URL')}/match/by-match-id/{match_id}')


async def report_match(match_id:str, match_data: dict):
    request_with_handle(method='POST', url=f'{os.getenv('NITZ_API_URL')}/reporter/match', params={'match_id': match_id}, json=match_data )
