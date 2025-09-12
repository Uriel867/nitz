from airflow.operators.python import get_current_context
import requests


def report(region: str):
    current_task = get_current_context()['ti'] # ti - current task instance
    summoners = current_task.xcom_pull(task_ids=f'scrape_{region}') #Pull the data from scrape node by region
    
    response = requests.post('http://api:8080/reporter/multiple',json=summoners) #report to mongodb
    response.raise_for_status() # raise an HTTP error if necessary