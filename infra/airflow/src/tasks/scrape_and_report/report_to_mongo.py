from airflow.operators.python import get_current_context
from airflow.exceptions import AirflowException
import requests
import os

nitz_api_url = os.getenv('NITZ_API_URL')

def report(region: str):
    current_task = get_current_context()['ti'] # ti - current task instance
    summoners = current_task.xcom_pull(task_ids=f'scrape_{region}') #Pull the data from scrape node by region
    
    response = requests.post(f'{nitz_api_url}/reporter/multiple',json=summoners) #report to mongodb
    
    if response.status_code != 200:
        raise AirflowException(f'reporting to mongo from {region} task failed')

       