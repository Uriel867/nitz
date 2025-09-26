from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta
from tasks.match_data_tree.get_matches_ids import fetch_all_summoners_task, fetch_first_summoner_puuid_task, fetch_matches_ids_task
from tasks.match_data_tree.report_matches_data import fetch_and_report_all_matches_task, fetch_and_report_chunk_task
from tasks.match_data_tree.matches_ids_chunks import make_chunks_task

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(seconds=10)
}

def triggerer():
    return True

with DAG(
    dag_id='matches_by_participants',
    default_args=default_args,
    catchup=False
) as dag:

    triggerer_task = PythonOperator(
        task_id='triggerer',
        python_callable=triggerer
    )

    summoner_list_task = PythonOperator(
        task_id='summoner_list',
        python_callable=fetch_all_summoners_task
    )

    get_first_summoner_puuid_task = PythonOperator(
        task_id='get_first_summoner_puuid',
        python_callable=fetch_first_summoner_puuid_task
    )

    match_tree_task = PythonOperator(
        task_id='fetch_matches_ids',
        python_callable=fetch_matches_ids_task,
        op_kwargs={'depth':1},
    )

    matches_ids_chunks_task = PythonOperator(
        task_id='matches_ids_chunks',
        python_callable=make_chunks_task
    )

    report_chunks = PythonOperator.partial(
        task_id='report_chunk',
        python_callable=fetch_and_report_chunk_task,
    ).expand(op_kwargs=matches_ids_chunks_task.output)


    triggerer_task >> summoner_list_task >> get_first_summoner_puuid_task >> match_tree_task >> matches_ids_chunks_task >> report_chunks