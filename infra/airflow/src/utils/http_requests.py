import asyncio
import aiohttp
import logging
from airflow.exceptions import AirflowException, AirflowFailException

RETRY_REQUESTS = [422, 429 , 500, 502, 504]
FAIL_REQUESTS = [404]
logger = logging.getLogger(__name__)
_TIMEOUT = aiohttp.ClientTimeout(total=900)  # 15 minutes overall timeout

async def request_with_handle(method: str, url: str, retries=20, **kwargs):
    for attempt in range(retries):
        try:
            async with aiohttp.ClientSession(timeout=_TIMEOUT) as session:
                #response = await session.request(method, url, **kwargs)
                async with session.request(method, url, **kwargs) as response:
                    response.raise_for_status()
                    if method == 'GET':
                        if await response.json() == None:
                            logger.error(f'Recieved None')
                        return await response.json()
                    return None # on successful POST request
        except aiohttp.ClientResponseError as e:
            if e.status == 503:
                await asyncio.sleep(1)
            if e.status == 422:
                logger.error(f"Failed to send this content: {kwargs.get('json')}")
            if e.status in FAIL_REQUESTS and attempt == retries - 1:
                raise AirflowFailException(f'Request failed with exception {e} - failing task') from e

            if e.status in RETRY_REQUESTS and attempt == retries - 1:
                raise AirflowException(f'API request failed with exception {e} - retrying ask') from e

        except asyncio.TimeoutError:
            if attempt== retries - 1:
                raise AirflowException(f'API request timed out for {method} {url}') from e

        await asyncio.sleep(1)



# 404 - fail, 429 - retry, 500 - retry, 502 - retry, 503 - retry, 504 - retry
