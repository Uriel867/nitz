import requests
from airflow.exceptions import AirflowException, AirflowFailException

RETRY_REQUESTS = [429 ,500, 502, 503,504]
FAIL_REQUESTS = [404]

def request_with_handle(method: str, url: str, **kwargs):
    response = None
    try:
        response = requests.request(method, url, **kwargs)
    except requests.exceptions.RequestException as e:
       if e.response.status_code in FAIL_REQUESTS:
           raise AirflowFailException(f'Request failed with exception {e} - failing task')

       if e.response.status_code in RETRY_REQUESTS:
           raise AirflowException(f'API request failed with exception {e} - retrying ask')

    if method == 'GET':
        return response.json()




# 404 - fail, 429 - retry, 500 - retry, 502 - retry, 503 - retry, 504 - retry