import requests
import time
import aiohttp
import asyncio

from includes import env

from airflow.sdk import DAG, task

# A DAG represents a workflow, a collection of tasks
with DAG(
    dag_id='scrape-load-transform', 
    catchup=False
) as dag:
    # global variables for the tasks in the DAG
    start_page = 1
    end_page = 250
    regions = ['br', 'eune', 'euw', 'jp', 'kr', 'lan', 'las', 'me', 'na', 'oce', 'ru', 'sea', 'tr', 'tw', 'vn']

    # initial task to trigger all scraping tasks
    @task(task_id='triggerer')
    def triggerer(**kwargs):
        return True

    @task(task_id='scrape')
    def scrape(start_page: int, end_page: int, region: str, **kwargs):
        query_params = {'start_page': start_page, 'end_page': end_page, 'region': region}
        response = requests.get(f'{env.API_URL}/scrape', params=query_params)
        json_data = response.json()
        # push status code to checkin later tasks if it was successful
        # kwargs['task_instance'].xcom_push(key='scrape_data', value=json_data)
        return json_data
    
    @task(task_id='load-to-mongodb')
    def load_to_mongodb(**kwargs):
        # getting the returned value from the scrape task
        scraped_data = kwargs['task_instance'].xcom_pull(task_ids='scrape', key='return_value')
        # reporting to mongo
        asyncio.run(report_summoners(scraped_data))


    # creating a list of scrape tasks for each region
    scrape_tasks = [
        scrape(start_page=start_page, end_page=end_page, region=region) for region in regions
    ]

    # setting the dependencies: triggerer -> all scrape tasks
    triggerer() >> scrape_tasks

    # setting the dependencies for the report & transform tasks: after all scrape tasks are done
    [task >> load_to_mongodb() for task in scrape_tasks]

async def report_summoners(data):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{env.API_URL}/reporter/multiple', json=data) as response:
                json_data = await response.json()
                return json_data
    except:
        return None

async def report_summoner(summoner_data, futures):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f'{env.API_URL}/scrape/reporter/summoner', params=summoner_data) as response:
                futures.append(await response.json())
    except:
        return None

async def await_futures(futures):
    await asyncio.gather(*futures)