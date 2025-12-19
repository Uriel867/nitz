import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from dags import default_args
from utils.make_chunks import make_chunks_task
from utils.fetch_and_report_data import fetch_and_report_chunk_task
from utils.fetch_all_summoners import fetch_all_summoners_task

def triggerer():
    return True


with DAG(
        dag_id='add_puuid',
        default_args=default_args,
        catchup=False
) as dag:

    triggerer_task = PythonOperator(
        task_id='triggerer',
        python_callable=triggerer
    )

    # scrape for each region
    fetch_all_summoners_task = PythonOperator(
        task_id='fetch_all_summoners',
        python_callable=fetch_all_summoners_task
    )

    make_chunks = PythonOperator(
        task_id='make_chunks',
        python_callable=make_chunks_task,
        op_kwargs={'task_id': 'fetch_all_summoners',
                   'chunk_size': 10},
    )

    report_chunks_task = PythonOperator.partial(
        task_id='report_chunk',
        python_callable=fetch_and_report_chunk_task,
    ).expand(
        op_kwargs=make_chunks.output.map(
            lambda chunk: {
                "chunk": chunk,
                "fetch_url": f'{os.getenv("NITZ_API_URL")}/account/by-id',
                "report_url": f'{os.getenv("NITZ_API_URL")}/reporter/summoner/add-puuid',
                "summoner": True,
                "match": False,
            }
        )
    )


    triggerer_task >> fetch_all_summoners_task >> make_chunks >> report_chunks_task
