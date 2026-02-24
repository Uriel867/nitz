from typing import List, Dict
import logging
import asyncio
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import get_current_context
from utils.fetch_all_summoners import fetch_all_summoners


logger = logging.getLogger("airflow.task")

def fetch_all_summoners_task():
    return asyncio.run(fetch_all_summoners())

def prepare_summoners_task():
    current_task = get_current_context()['ti']
    summoners = current_task.xcom_pull(task_ids='all_summoner_list') # all summoners list

    return asyncio.run(prepare_summoners(summoners))

# prepare the summoner data that will be inserted into postgres
async def prepare_summoners(summoners: List[Dict]):
    rows_to_insert = []

    for summoner in summoners:
        # not inserting to postgres if puuid is missing
        if 'puuid' not in summoner.keys():
            continue

        game_name = summoner['game_name']
        tag_line = summoner['tag_line']
        region = summoner['region']
        sub_region = summoner['sub_region']
        puuid = summoner['puuid']

        rows_to_insert.append((
            puuid,
            game_name,
            tag_line,
            region,
            sub_region
        ))
    return rows_to_insert


def insert_summoners_to_postgres_task():
    current_task = get_current_context()['ti']  # ti - current task instance
    rows_to_insert = current_task.xcom_pull(task_ids='prepare_summoners') # list of all summoners to insert

    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    target_table = 'api.summoner_info'
    target_columns = ['puuid', 'game_name', 'tag_line', 'region', 'sub_region']

    pg_hook.insert_rows(
        table=target_table,
        rows=rows_to_insert,
        target_fields=target_columns,
        commit_every=1000
    )
