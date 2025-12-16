import os
import asyncio
from airflow.models import Variable
from utils.http_requests import request_with_handle

start_page = Variable.get('START_PAGE', default_var=1)
end_page = Variable.get('END_PAGE', default_var=1)


SUB_REGIONS = [
    'br',
    'eune',
    'euw',
    'jp',
    'kr',
    'lan',
    'las',
    #'me', not working for now
    'na',
 #   'oce', not working for now
    'ru',
    'sea',
    'tr',
    'tw',
    'vn'
]

def scrape(start_page: int, end_page: int, sub_region: str):
    query_params = {
        'start_page': start_page,
        'end_page': end_page,
        'sub_region': sub_region
    }
    return asyncio.run(scrape_pages(query_params))

async def scrape_pages(query_params: dict):
    return await request_with_handle(method='GET', url=f'{os.getenv("NITZ_API_URL")}/scrape', params=query_params)
