import asyncio
import logging
import aiohttp
from airflow.exceptions import AirflowException, AirflowFailException

RETRY_REQUESTS = [422, 429 , 500, 502, 503, 504]
FAIL_REQUESTS = [404]
logger = logging.getLogger("airflow.task") # using this to print into the airflow ui
_TIMEOUT = aiohttp.ClientTimeout(total=900)  # 15 minutes overall timeout
retries = 10

async def request_with_handle(method: str, url: str, **kwargs):
    for attempt in range(retries):
        try:
            async with aiohttp.ClientSession(timeout=_TIMEOUT) as session:
                async with session.request(method, url, **kwargs) as response:

                    response.raise_for_status()
                    if method == 'GET':
                        return await response.json()
                    return None # on successful POST request

        except aiohttp.ClientResponseError as e:

            if e.status in FAIL_REQUESTS and attempt == retries - 1:
                raise AirflowFailException(f'Request failed with exception {e} - failing task') from e

            if e.status in RETRY_REQUESTS and attempt == retries - 1:
                raise AirflowException(f'API request failed with exception {e} - retrying ask') from e



        except asyncio.TimeoutError:
            if attempt== retries - 1:
                raise AirflowException(f'API request timed out for {method} {url}') from e

        wait_time = 2 ** attempt # exponential backoff - each attempt makes it wait longer before the next call
        await asyncio.sleep(wait_time)

    raise AirflowException(f"All {retries} retry attempts failed for {method} {url}.")

# 404 - fail, 429 - retry, 500 - retry, 502 - retry, 503 - retry, 504 - retry
