import asyncio
import aiohttp
from airflow.exceptions import AirflowException, AirflowFailException

RETRY_REQUESTS = [429 ,500, 502, 503,504]
FAIL_REQUESTS = [404]

_TIMEOUT = aiohttp.ClientTimeout(total=900)  # 15 minutes overall timeout

async def request_with_handle(method: str, url: str, retries=5, **kwargs):
    for attempt in range(retries):
        try:
            async with aiohttp.ClientSession(timeout=_TIMEOUT) as session:
                #response = await session.request(method, url, **kwargs)
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

        await asyncio.sleep(1)






# 404 - fail, 429 - retry, 500 - retry, 502 - retry, 503 - retry, 504 - retry
