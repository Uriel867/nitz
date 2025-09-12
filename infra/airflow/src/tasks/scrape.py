import requests
from airflow.models import Variable


start_page = Variable.get('start_page', default_var=1)
end_page = Variable.get('end_page', default_var=10)


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

def scrape(start_page: int, end_page: int, region: str):
    query_params = {
        'start_page': start_page,
        'end_page': end_page,
        'region': region
    }
    response = requests.get('http://api:8080/scrape', params=query_params)
    response.raise_for_status() # raise an HTTP error if necessary
  
    return response.json()