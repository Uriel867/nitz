from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow import DAG
from airflow.operators.python import PythonOperator
from dags import triggerer


with DAG(
    dag_id='postgres_etl',
    catchup=False,
) as dag:

    triggerer_task = PythonOperator(
        task_id='triggerer_task',
        python_callable=triggerer,
    )

    insert = SQLExecuteQueryOperator(
        task_id='insert',
        conn_id="postgres_default",
        sql='sql/test.sql'
    )
    triggerer_task >> insert