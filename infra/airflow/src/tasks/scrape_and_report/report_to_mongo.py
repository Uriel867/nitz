from airflow.operators.python import get_current_context
from airflow.exceptions import AirflowException
from utils.exceptions import request_with_handle
import requests
import os


def report(region: str):
    current_task = get_current_context()['ti'] # ti - current task instance
    summoners = current_task.xcom_pull(task_ids=f'scrape_{region}') #Pull the data from scrape node by region

    request_with_handle(method='POST', url=f'{os.getenv('NITZ_API_URL')}/reporter/multiple', json=summoners)
