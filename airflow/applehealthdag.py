from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
from normalize_json import normalize_json, cleanup
from populate_rds import populate_rds

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2020, 11, 8),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'applehealth_dag',
    default_args=default_args,
    description='DAG to orchestrate AWS services',
    schedule_interval=timedelta(days=1),
)

s3_to_csv = PythonOperator(
    task_id='s3_to_csv',
    python_callable=normalize_json,
    dag=dag, 
)

csv_to_rds = PythonOperator(
    task_id='csv_to_rds',
    python_callable=populate_rds,
    dag=dag, 
)

clean_files = PythonOperator(
    task_id='clean_files',
    python_callable=cleanup,
    dag=dag, 
)

s3_to_csv >> csv_to_rds >> clean_files