import requests
from airflow.operators.python import get_current_context
from airflow.exceptions import AirflowException
import os

nitz_api_url = os.getenv('NITZ_API_URL')

def report_matches_to_mongo():
    current_task = get_current_context()['ti']
    matches_ids = current_task.xcom_pull(task_ids='match_tree')

    for match_id in matches_ids:
        match_data = requests.get(f'{nitz_api_url}/match/by-match-id/{match_id}').json()
        if match_data.status_code != 200:
            raise AirflowException(f'Error getting match data for {match_id}')

        response = requests.post(f'{nitz_api_url}/reporter/match', params={'match_id': match_id}, json=match_data)
        if response.status_code != 200:
            raise AirflowException(f'Reporting match id {match_id} failed with status code {response.status_code}')


