import os
import asyncio
from typing import List
from airflow.exceptions import AirflowException
from airflow.operators.python import get_current_context
from utils.http_requests import request_with_handle
from utils.fetch_puuid import fetch_puuid

# returns a list of all summoners in mongodb
def fetch_all_summoners_task():
    return asyncio.run(fetch_all_summoners())

async def fetch_all_summoners():
    return await request_with_handle('GET', f'{os.getenv("NITZ_API_URL")}/reporter/all')

# returns the first summoner in the summoners list
def fetch_first_summoner_puuid_task():
    current_task = get_current_context()['ti']  # ti - current task instance
    summoners = current_task.xcom_pull(task_ids='all_summoner_list')
    return asyncio.run(fetch_first_summoner_puuid(summoners))

async def fetch_first_summoner_puuid(summoners: List[str]):
    if summoners is None:
        raise AirflowException('Summoner list is empty')

    region = summoners[0]['region']
    tag_line = summoners[0]['tag_line']
    summoner_name = summoners[0]['game_name']

    puuid = await fetch_puuid(tag_line, summoner_name, region)

    return {"puuid": puuid, "region": region}

def fetch_first_summoner_matches_task():
    current_task = get_current_context()['ti']  # ti - current task instance
    first_summoner = current_task.xcom_pull(task_ids='fetch_first_summoner_puuid')
    puuid = first_summoner['puuid']
    region = first_summoner['region']

    return asyncio.run(fetch_first_summoner_matches(puuid, region))

async def fetch_first_summoner_matches(puuid: str, region: str):
    return await request_with_handle(method='GET', url=f'{os.getenv("NITZ_API_URL")}/match/by-puuid/{puuid}', params={'region': region})


# returns the participants puuids of a match
async def fetch_match_participants(match_id: str, region: str):
    match_data = await request_with_handle(method='GET', url=f'{os.getenv("NITZ_API_URL")}/match/by-match-id/{match_id}', params={'region': region})
    match_participants = match_data['metadata']['participants']

    return match_participants

def fetch_matches_ids_task(depth: int):
    current_task = get_current_context()['ti']  # ti - current task instance
    first_summoner = current_task.xcom_pull(task_ids='fetch_first_summoner_puuid')
    region = first_summoner['region']

    return asyncio.run(fetch_matches_ids(depth, region))


# gathers matches ids by collecting matches from different summoners
async def fetch_matches_ids(depth: int, region: str):
    current_task = get_current_context()['ti']  # ti - current task instance
    matches_ids = current_task.xcom_pull(task_ids='fetch_first_summoner_matches')
    root_puuid = current_task.xcom_pull(task_ids='fetch_first_summoner_puuid') # starting from this summoner

    matches_participants = []
    seen_puuids = {root_puuid["puuid"]}
    seen_matches = set()
    match_ids_index  = 0 # tracks length of matches_ids
    matches_participants_index = 0 # tracks length of matches_participants

    # how deep we want the matches ids "tree" to be
    while depth > 0:
        match_ids_index = await fetch_puuids_from_matches(matches_ids, seen_puuids, matches_participants, match_ids_index, region)
        matches_participants_index = await fetch_matches_ids_from_participants(matches_ids, matches_participants, seen_matches, matches_participants_index, region)
        depth -= 1

    return matches_ids

# iterates over all matches we have and extracts participants from each one
async def fetch_puuids_from_matches(matches_ids: List[str], seen_puuids: set[str], matches_participants: List[str], index: int, region: str):
    while index < len(matches_ids):
        for puuid in await fetch_match_participants(matches_ids[index], region):
            if puuid not in seen_puuids:
                seen_puuids.add(puuid)
                matches_participants.append(puuid)
        index += 1
    return index

# iterates over the participants we gathered and extracts their latest matches ids
async def fetch_matches_ids_from_participants(matches_ids: List[str], matches_participants: List[str], seen_matches: set[str], index: int, region):
    while index < len(matches_participants):
        for match_id in await fetch_first_summoner_matches(matches_participants[index], region):
            if match_id not in seen_matches and '_' in match_id:
                seen_matches.add(match_id)
                matches_ids.append(match_id)
        index += 1
    return index
