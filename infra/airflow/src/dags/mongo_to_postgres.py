from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from dags import default_args

def trigerrer():
    return True

with DAG(
    dag_id='mongo_to_postgres',
    default_args=default_args,
    catchup=False
) as dag:

    triggerer_task = PythonOperator(
        task_id='triggerer',
        python_callable=trigerrer
    )

    run_my_query = SQLExecuteQueryOperator(
        task_id="run_my_query",

        # Airflow automatically finds the connection you defined
        # in the environment variable.
        conn_id="postgres_default",

        sql="INSERT INTO api.summoner_info (puuid, game_name, tag_line) VALUES ('some-unique-puuid-12345', 'MyGameName', 'MyTag');",
    )