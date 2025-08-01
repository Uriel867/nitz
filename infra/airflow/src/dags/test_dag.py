from datetime import datetime

from airflow.sdk import DAG, task
from airflow.providers.standard.operators.bash import BashOperator

# A DAG represents a workflow, a collection of tasks
with DAG(dag_id="demo", start_date=datetime(2025, 1, 1), schedule="0 0 * * *") as dag:
    @task()
    def airflow():
        import requests
        import json
        response = requests.get('http://api:8080/scrape')
        return json.loads(response.content)

    # Set dependencies between tasks
    airflow()