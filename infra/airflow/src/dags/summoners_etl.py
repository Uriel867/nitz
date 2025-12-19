from airflow import DAG
from airflow.operators.python import PythonOperator
from dags import default_args
from tasks.summoners_etl.summoners_etl import (
    fetch_all_summoners_task,
    prepare_summoners_task,
    insert_summoners_to_postgres_task
)

def triggerer():
    return True

with DAG(
        dag_id='summoners_etl',
        default_args=default_args,
        catchup=False,

) as dag:

    triggerer_task = PythonOperator(
        task_id='triggerer',
        python_callable=triggerer,
    )

    all_summoner_list_task = PythonOperator(
        task_id='all_summoner_list',
        python_callable=fetch_all_summoners_task
    )


    prepare_summoners_task = PythonOperator(
        task_id='prepare_summoners',
        python_callable=prepare_summoners_task
    )

    # Task 3: Insert the prepared data into Postgres
    insert_summoners_task = PythonOperator(
        task_id='insert_summoners_to_postgres',
        python_callable=insert_summoners_to_postgres_task
    )

    # Set the dependencies
    triggerer_task >> all_summoner_list_task >> prepare_summoners_task >> insert_summoners_task
