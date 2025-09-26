from airflow.exceptions import AirflowException
from airflow.operators.python import get_current_context
from utils.http_requests import request_with_handle
import os
import asyncio

def fetch_all_summoners_task():
    return asyncio.run(fetch_all_summoners())

async def fetch_all_summoners():
    return await request_with_handle('GET', f'{os.getenv('NITZ_API_URL')}/reporter/all')


async def fetch_puuid(tag_line: str, summoner_name: str, region: str):
    summoner_data = await request_with_handle('GET', f'{os.getenv('NITZ_API_URL')}/account/{region}/{summoner_name}/{tag_line}')
    return summoner_data['puuid']

def fetch_first_summoner_puuid_task():
    current_task = get_current_context()['ti']  # ti - current task instance
    summoners = current_task.xcom_pull(task_ids='summoner_list')
    return asyncio.run(fetch_first_summoner_puuid(summoners))

async def fetch_first_summoner_puuid(summoners):
    if summoners is None:
        raise AirflowException('Summoner list is empty')

    region = summoners[0]['region']
    tag_line = summoners[0]['tag_line']
    summoner_name = summoners[0]['game_name']

    puuid = await fetch_puuid(tag_line, summoner_name, region)

    return puuid


async def fetch_summoner_matches(puuid):
    return await request_with_handle('GET', f'{os.getenv('NITZ_API_URL')}/match/by-puuid/{puuid}')


async def fetch_match_participants(match_id):
    match_data = await request_with_handle('GET', f'{os.getenv('NITZ_API_URL')}/match/by-match-id/{match_id}')
    match_participants = match_data['metadata']['participants']

    return match_participants

def fetch_matches_ids_task(depth):
    current_task = get_current_context()['ti']  # ti - current task instance
    root_puuid = current_task.xcom_pull(task_ids='get_first_summoner_puuid')

    matches_ids = asyncio.run(fetch_summoner_matches(root_puuid))
    matches_participants = []
    seen_puuids = {root_puuid}
    seen_matches = set()
    match_ids_index  = 0
    matches_participants_index = 0

    while depth > 0:
        match_ids_index = fetch_puuids_from_matches(matches_ids, seen_puuids, matches_participants, match_ids_index)
        matches_participants_index = fetch_matches_ids_from_participants(matches_ids, matches_participants, seen_matches, matches_participants_index)
        depth -= 1

    return matches_ids

def fetch_puuids_from_matches(matches_ids, seen_puuids, matches_participants, index):
    while index < len(matches_ids):
        for puuid in asyncio.run(fetch_match_participants(matches_ids[index])):
            if puuid not in seen_puuids:
                seen_puuids.add(puuid)
                matches_participants.append(puuid)
        index += 1
    return index

def fetch_matches_ids_from_participants(matches_ids, matches_participants, seen_matches, index):
    while index < len(matches_participants):
        for match_id in asyncio.run(fetch_summoner_matches(matches_participants[index])):
            if match_id not in seen_matches and '_' in match_id:
                seen_matches.add(match_id)
                matches_ids.append(match_id)
        index += 1
    return index