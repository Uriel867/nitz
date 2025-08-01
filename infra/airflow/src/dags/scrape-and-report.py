from datetime import datetime
import requests
import json

from airflow.sdk import DAG, task

# A DAG represents a workflow, a collection of tasks
with DAG(
    dag_id='scrape-and-report', 
    start_date=datetime(2025, 1, 1), 
    # every day at 00:00
    schedule="0 0 * * *", 
    catchup=False
) as dag:
    # global variables for the tasks in the DAG
    start_page = 1
    end_page = 100
    regions = ['br', 'eune', 'euw', 'jp', 'kr', 'lan', 'las', 'me', 'na', 'oce', 'ru', 'sea', 'tr', 'tw', 'vn']

    # initial task to trigger all scraping tasks
    @task(task_id='triggerer')
    def triggerer(**kwargs):
        return True

    @task(task_id='scrape')
    def scrape(start_page: int, end_page: int, region: str, **kwargs):
        query_params = {'start_page': start_page, 'end_page': end_page, 'region': region}
        response = requests.get('http://api:8080/scrape', params=query_params)
        json_data = response.json()
        kwargs['task_instance'].xcom_push(key='scrape_data', value=json_data)
        return json_data
    
    @task(task_id='report-to-mongodb')
    def report_to_mongodb(**kwargs):
        # getting the returned value from the scrape task
        scraped_data = kwargs['task_instance'].xcom_pull(task_ids='scrape', key='return_value')
        # reporting to mongo (TODO: make it asynchronous)
        response = requests.post('http://api:8080/reporter/multiple', json=scraped_data)
        if response.status_code == 200:
            return response.json()
        return response.content
    
    @task(task_id='report-to-postgres')
    def report_to_postgres(**kwargs):
        scraped_data = kwargs['task_instance'].xcom_pull(task_ids='scrape', key='return_value')
        # TODO: implement reporting to postgres
        return True


    # creating a list of scrape tasks for each region
    scrape_tasks = [
        scrape(start_page=start_page, end_page=end_page, region=region) for region in regions
    ]

    # setting the dependencies: triggerer -> all scrape tasks
    triggerer() >> scrape_tasks

    # setting the dependencies for the report tasks: after all scrape tasks are done
    [task >> report_to_mongodb() for task in scrape_tasks]
    [task >> report_to_postgres() for task in scrape_tasks]
