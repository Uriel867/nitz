import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from dags import default_args
from tasks.match_data_tree.fetch_matches_ids import (
    fetch_all_summoners_task, fetch_first_summoner_puuid_task, fetch_matches_ids_task,
    fetch_first_summoner_matches_task)
from utils.make_chunks import make_chunks_task
from utils.fetch_and_report_data import fetch_and_report_chunk_task

def triggerer():
    return True

with (DAG(
    dag_id='matches_by_participants',
    default_args=default_args,
    catchup=False
) as dag):

    triggerer_task = PythonOperator(
        task_id='triggerer',
        python_callable=triggerer
    )

    all_summoner_list_task = PythonOperator(
        task_id='all_summoner_list',
        python_callable=fetch_all_summoners_task
    )

    fetch_first_summoner_puuid_task = PythonOperator(
        task_id='fetch_first_summoner_puuid',
        python_callable=fetch_first_summoner_puuid_task
    )

    fetch_first_summoner_matches_task = PythonOperator(
        task_id='fetch_first_summoner_matches',
        python_callable=fetch_first_summoner_matches_task
    )

    match_tree_task = PythonOperator(
        task_id='fetch_matches_ids',
        python_callable=fetch_matches_ids_task,
        op_kwargs={'depth': 1},
    )

    matches_ids_chunks_task = PythonOperator(
        task_id='matches_ids_chunks',
        python_callable=make_chunks_task,
        op_kwargs={'task_id': 'fetch_matches_ids',
                   'chunk_size': 10},
    )

    report_chunks_task = PythonOperator.partial(
        task_id='report_chunk',
        python_callable=fetch_and_report_chunk_task,
    ).expand(
        op_kwargs=matches_ids_chunks_task.output.map(
            lambda chunk: {
                "chunk": chunk,
                "fetch_url": f'{os.getenv("NITZ_API_URL")}/match/by-match-id',
                "report_url": f'{os.getenv("NITZ_API_URL")}/reporter/match',
                "summoner": False,
                "match": True,
            }
        )
    )


    triggerer_task >> all_summoner_list_task >> fetch_first_summoner_puuid_task >> fetch_first_summoner_matches_task >> match_tree_task >> matches_ids_chunks_task >> report_chunks_task
