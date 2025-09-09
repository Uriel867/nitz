from typing import Dict, List
from airflow import DAG
from airflow.operators.python import PythonOperator,get_current_context
from airflow.models import Variable
from datetime import timedelta
import requests

start_page = Variable.get('start_page', default_var=1)
end_page = Variable.get('end_page', default_var=10)


default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

regions = [
    'br',
    'eune',
    'euw',
    'jp',
    'kr',
    'lan',
    'las',
    'me',
    'na',
    'oce',
    'ru',
    'sea',
    'tr',
    'tw',
    'vn'
]

def triggerer():
    return True

def scrape(start_page: int, end_page: int, region: str):
    query_params = {
        'start_page': start_page,
        'end_page': end_page,
        'region': region
    }
    response = requests.get('http://api:8080/scrape', params=query_params)
    response.raise_for_status() # raise an HTTP error if necessary
  
    return response.json()

def report(region: str):
    current_task = get_current_context()['ti'] # ti - current task instance
    summoners = current_task.xcom_pull(task_ids=f'scrape_{region}') #Pull the data from scrape node by region
    
    response = requests.post('http://api:8080/reporter/multiple',json=summoners) #report to mongodb
    response.raise_for_status() # raise an HTTP error if necessary

 
with DAG(
    dag_id='scrape_load_transform',
    default_args=default_args,
    catchup=False
) as dag:
    
    triggerer_task = PythonOperator(
        task_id='triggerer',
        python_callable=triggerer
    )
    
    #scrape for each region
    for region in regions:
        scrape_task = PythonOperator(
            task_id=f'scrape_{region}',
            python_callable=scrape,
            op_kwargs={
                'start_page': start_page,
                'end_page': end_page,
                'region': region,
            },
        )

        #report for each region
        report_task = PythonOperator(
            task_id=f'report_{region}',
            python_callable=report,
            op_kwargs={'region': region},
        )

        # Airflow runs them in a parallel way and not one by one 
        triggerer_task >> scrape_task >> report_task