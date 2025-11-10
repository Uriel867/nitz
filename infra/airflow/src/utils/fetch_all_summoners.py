import os
from .http_requests import request_with_handle

async def fetch_all_summoners():
    return await request_with_handle('GET', f'{os.getenv("NITZ_API_URL")}/reporter/all')