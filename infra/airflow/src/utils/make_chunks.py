from airflow.operators.python import get_current_context

def make_chunks_task(task_id: str, chunk_size: int = 10):
    current_task = get_current_context()['ti']  # ti - current task instance
    to_be_chunked = current_task.xcom_pull(task_ids=task_id)

    chunks = [to_be_chunked[i:i + chunk_size] for i in range(0, len(to_be_chunked), chunk_size)]
    return [{'data': chunk} for chunk in chunks]