import os
import asyncio
from airflow.operators.python import get_current_context
from utils.http_requests import request_with_handle


def report_summoners_task(sub_region: str):
    current_task = get_current_context()['ti']  # ti - current task instance
    summoners = current_task.xcom_pull(task_ids=f'scrape_{sub_region}')  # Pull the data from scrape node by region
    asyncio.run(report_summoners(summoners))

async def report_summoners(summoners: list):
    await request_with_handle(method='POST', url=f'{os.getenv("NITZ_API_URL")}/reporter/multiple', json=summoners)
