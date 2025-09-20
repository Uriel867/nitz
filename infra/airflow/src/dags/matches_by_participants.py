from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta
from tasks.match_data_tree.get_matches_data import get_summoner_list, get_first_summoner_puuid, get_matches_ids
from tasks.match_data_tree.report_matches import report_matches_to_mongo

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

    get_first_summoner_puuid_task = PythonOperator(
        task_id='get_first_summoner_puuid',
        python_callable=get_first_summoner_puuid
    )

    match_tree_task = PythonOperator(
        task_id='match_tree',
        python_callable=get_matches_ids,
        op_kwargs={'depth':0},
    )

    report_to_mongo_task = PythonOperator(
        task_id='report_to_mongo',
        python_callable=report_matches_to_mongo,
    )


    triggerer_task >> summoner_list_task >> get_first_summoner_puuid_task >> match_tree_task >> report_to_mongo_task