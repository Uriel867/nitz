import requests
from airflow.operators.python import get_current_context

def get_summoner_list():
    response = requests.get('http://api:8080/reporter/all')
    
    return response.json()

def get_summoner_puuid():
    current_task = get_current_context()['ti']  # ti - current task instance
    summoners = current_task.xcom_pull(task_ids=f'summoner_list')
    region = summoners[0]['region']
    tag_line = summoners[0]['tag_line']
    summoner_name = summoners[0]['game_name']


    response = requests.get(f'http://api:8080/account/{region}/{summoner_name}/{tag_line}')

    data = response.json()

    return data['puuid']

def get_summoner_matches():
    puuid = get_summoner_puuid()

    response = requests.get(f'http://api:8080/match/by-puuid/{puuid}')

    return response.json()

def get_match_participants():
    current_task = get_current_context()['ti']  # ti - current task instance
    matches = current_task.xcom_pull(task_ids=f'summoner_matches')
    match_id = matches[0]

    response = requests.get(f'http://api:8080/match/by-match-id/{match_id}')
    match_data = response.json()

    match_participants = match_data['metadata']['participants']

    return match_participants