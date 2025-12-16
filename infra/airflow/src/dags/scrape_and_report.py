from airflow import DAG
from airflow.operators.python import PythonOperator
from dags import default_args
from tasks.scrape_and_report.scrape import SUB_REGIONS, scrape, start_page, end_page
from tasks.scrape_and_report.report_summoners import report_summoners_task


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

    # scrape for each region
    for sub_region in SUB_REGIONS:
        scrape_task = PythonOperator(
            task_id=f'scrape_{sub_region}',
            python_callable=scrape,
            op_kwargs={
                'start_page': start_page,
                'end_page': end_page,
                'sub_region': sub_region,
            },
        )

        # report for each region
        report_task = PythonOperator(
            task_id=f'report_{sub_region}',
            python_callable=report_summoners_task,
            op_kwargs={'sub_region': sub_region},
        )

        # Airflow runs them in a parallel way and not one by one
        triggerer_task >> scrape_task >> report_task
