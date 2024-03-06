from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from packages.crypto_data_consumer import consume_and_store_data

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2022, 1, 1),
    "email": ["your-email@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "crypto_data_consumer",
    default_args=default_args,
    description="A DAG to consume crypto data from Kafka and store in PostgreSQL",
    schedule_interval=timedelta(hours=1),
)

t1 = PythonOperator(
    task_id="consume_and_store_data",
    python_callable=consume_and_store_data,
    dag=dag,
)
