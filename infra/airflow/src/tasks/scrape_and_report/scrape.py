import requests
from airflow.models import Variable
from airflow.exceptions import AirflowException
from utils.exceptions import request_with_handle
import os

start_page = Variable.get('START_PAGE', default_var=1)
end_page = Variable.get('END_PAGE', default_var=1)


REGIONS = [
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

def scrape(start_page: int, end_page: int, region: str):
    query_params = {
        'start_page': start_page,
        'end_page': end_page,
        'region': region
    }
    return request_with_handle(method='GET',url=f'{os.getenv('NITZ_API_URL')}/scrape', params=query_params)