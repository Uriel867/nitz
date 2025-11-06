from airflow.operators.python import get_current_context

# splits matches ids list into chunks in order to have a separate task for each chunk
def make_chunks_task(chunk_size: int = 10):
    current_task = get_current_context()['ti']  # ti - current task instance
    matches_ids = current_task.xcom_pull(task_ids='fetch_matches_ids')

    chunks = [matches_ids[i:i + chunk_size] for i in range(0, len(matches_ids), chunk_size)]
    return [{'matches_ids_chunk': chunk} for chunk in chunks]
