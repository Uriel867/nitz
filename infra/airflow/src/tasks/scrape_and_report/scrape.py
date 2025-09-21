import requests
from airflow.models import Variable
from airflow.exceptions import AirflowException
import os

start_page = Variable.get('START_PAGE', default_var=1)
end_page = Variable.get('END_PAGE', default_var=1)
nitz_api_url = os.getenv('NITZ_API_URL')


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
    
    response = requests.get(f'{nitz_api_url}/scrape', params=query_params)

    if response.status_code != 200:
        raise AirflowException(f'scraping {region} task failed')

    return response.json()