from utils.fetch_all_summoners import fetch_all_summoners
import asyncio

def fetch_all_summoners_task():
    asyncio.run(fetch_all_summoners())

