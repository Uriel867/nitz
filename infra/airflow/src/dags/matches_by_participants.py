from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta
from tasks.match_data_tree.get_matches_ids import fetch_all_summoners_task, fetch_first_summoner_puuid_task, fetch_matches_ids_task
from tasks.match_data_tree.report_matches_data import fetch_and_report_all_matches_task

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
        task_id='match_tree',
        python_callable=fetch_matches_ids_task,
        op_kwargs={'depth':1},
    )

    report_to_mongo_task = PythonOperator(
        task_id='report_to_mongo',
        python_callable=fetch_and_report_all_matches_task,
    )


    triggerer_task >> summoner_list_task >> get_first_summoner_puuid_task >> match_tree_task >> report_to_mongo_task