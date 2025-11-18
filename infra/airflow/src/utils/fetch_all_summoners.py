import os
from .http_requests import request_with_handle
import logging

logger = logging.getLogger(__name__)

async def fetch_all_summoners():
    all_summoners =  await request_with_handle('GET', f'{os.getenv("NITZ_API_URL")}/reporter/all')
    logger.info(f'Retrieved {len(all_summoners)} summoners')
    return all_summoners