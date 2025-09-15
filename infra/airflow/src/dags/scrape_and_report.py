from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta
from tasks.scrape_and_report.scrape import REGIONS, scrape, start_page, end_page
from tasks.scrape_and_report.report_to_mongo import report as report_to_mongo


default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(seconds=10)
}

def triggerer():
    return True

with DAG(
    dag_id='scrape_load_transform',
    default_args=default_args,
    catchup=False
) as dag:
    
    triggerer_task = PythonOperator(
        task_id='triggerer',
        python_callable=triggerer
    )
    
    #scrape for each region
    for region in REGIONS:
        scrape_task = PythonOperator(
            task_id=f'scrape_{region}',
            python_callable=scrape,
            op_kwargs={
                'start_page': start_page,
                'end_page': end_page,
                'region': region,
            },
        )

        #report for each region
        report_task = PythonOperator(
            task_id=f'report_{region}',
            python_callable=report_to_mongo,
            op_kwargs={'region': region},
        )

        # Airflow runs them in a parallel way and not one by one 
        triggerer_task >> scrape_task >> report_task