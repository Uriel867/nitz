import requests
from airflow.operators.python import get_current_context
from airflow.exceptions import AirflowException
import os

from eventlet.green.http.client import responses


#iterate through the list of matches and report each one
def report_matches_to_mongo():
    current_task = get_current_context()['ti']
    matches_ids = current_task.xcom_pull(task_ids='match_tree')

    for match_id in matches_ids:
        match_data = get_match_data(match_id)
        report_match(match_id, match_data)


def get_match_data(match_id: str):
    try:
        response = requests.get(f'{os.getenv('NITZ_API_URL')}/match/by-match-id/{match_id}')
        if response.status_code != 200:
            raise AirflowException(f'Error getting match data for {match_id}')

    except Exception as e:
        raise AirflowException(f'API request failed with exception {e}')

    return response.json()

def report_match(match_id:str, match_data: dict):
    try:
        response = requests.post(f'{os.getenv('NITZ_API_URL')}/reporter/match', params={'match_id': match_id}, json=match_data)
        if response.status_code != 200:
            raise AirflowException(f'Reporting match id {match_id} failed with status code {response.status_code}')

    except Exception as e:
        raise AirflowException(f'API request failed with exception {e}')