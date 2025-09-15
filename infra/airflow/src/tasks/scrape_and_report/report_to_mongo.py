from airflow.operators.python import get_current_context
from airflow.exceptions import AirflowException
import requests


def report(region: str):
    current_task = get_current_context()['ti'] # ti - current task instance
    summoners = current_task.xcom_pull(task_ids=f'scrape_{region}') #Pull the data from scrape node by region
    
    response = requests.post('http://api:8080/reporter/multiple',json=summoners) #report to mongodb
    
    if response.status_code != 200:
        raise AirflowException(f'reporting to mongo from {region} task failed')

       