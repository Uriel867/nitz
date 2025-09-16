from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta
from tasks.match_data_tree.get_summoner import *

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
        python_callable=get_summoner_list
    )

    summoner_puuid_task = PythonOperator(
        task_id='summoner_puuid',
        python_callable=get_summoner_puuid
    )

    summoner_matches_task = PythonOperator(
        task_id='summoner_matches',
        python_callable=get_summoner_matches
    )

    match_participants_task = PythonOperator(
        task_id='match_participants',
        python_callable=get_match_participants
    )

    triggerer_task >> summoner_list_task >> summoner_puuid_task >> summoner_matches_task >> match_participants_task