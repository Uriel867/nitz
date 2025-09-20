import requests
from airflow.operators.python import get_current_context
from airflow.exceptions import AirflowException

def report_matches_to_mongo():
    current_task = get_current_context()['ti']
    matches_ids = current_task.xcom_pull(task_ids='match_tree')

    for match_id in matches_ids:
        match_data = requests.get(f'http://api:8080/match/by-match-id/{match_id}').json()
        print('match_data is:', match_data)
        response = requests.post('http://api:8080/reporter/match', params={'match_id': match_id}, json=match_data)

        if response.status_code != 200:
            raise AirflowException(f'Reporting match id {match_id} failed with status code {response.status_code}')


