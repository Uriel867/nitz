import requests
from airflow.exceptions import AirflowException
from airflow.operators.python import get_current_context
from utils.exceptions import request_with_handle
import os


def get_summoner_list():
    return request_with_handle('GET', f'{os.getenv('NITZ_API_URL')}/reporter/all')


def get_puuid(tag_line: str,summoner_name: str, region: str):
    summoner_data = request_with_handle('GET', f'{os.getenv('NITZ_API_URL')}/account/{region}/{summoner_name}/{tag_line}')

    return summoner_data['puuid']

def get_first_summoner_puuid():
    current_task = get_current_context()['ti']  # ti - current task instance
    summoners = current_task.xcom_pull(task_ids='summoner_list')

    if summoners is None:
        raise AirflowException('Summoner list is empty')

    region = summoners[0]['region']
    tag_line = summoners[0]['tag_line']
    summoner_name = summoners[0]['game_name']

    puuid = get_puuid(tag_line, summoner_name, region)

    return puuid


def get_summoner_matches(puuid):
    return request_with_handle('GET', f'{os.getenv('NITZ_API_URL')}/match/by-puuid/{puuid}')


def get_match_participants(match_id):
    match_data =request_with_handle('GET', f'{os.getenv('NITZ_API_URL')}/match/by-match-id/{match_id}')
    match_participants = match_data['metadata']['participants']

    return match_participants

def get_matches_ids(depth):
    current_task = get_current_context()['ti']  # ti - current task instance
    root_puuid = current_task.xcom_pull(task_ids='get_first_summoner_puuid')


    matches_ids = get_summoner_matches(root_puuid)
    matches_puuids = []
    seen_puuids = {root_puuid}
    seen_matches = set()

    while depth > 0:
        matches_puuids.extend(puuid
                              for match_id in matches_ids
                              for puuid in get_match_participants(match_id) if puuid not in seen_puuids
        )
        seen_puuids.update(matches_puuids)

        matches_ids.extend(match_id
                           for puuid in matches_puuids
                           for match_id in get_summoner_matches(puuid) if match_id not in seen_matches and '_' in match_id
        )
        seen_matches.update(matches_ids)

        depth -= 1

    return matches_ids