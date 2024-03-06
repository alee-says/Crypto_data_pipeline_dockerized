from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from packages.crypto_data_producer import fetch_and_send_crypto_data

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

dag1 = DAG(
    "crypto_data_producer_live_data",
    default_args=default_args,
    description="A DAG to fetch live crypto data and send to Kafka",
    schedule_interval=timedelta(hours=1),
)

dag2 = DAG(
    "crypto_data_producer_non_changing_data",
    default_args=default_args,
    description="A DAG to fetch non-changing crypto data and send to Kafka",
    schedule_interval=timedelta(days=1),
)

t1 = PythonOperator(
    task_id="fetch_and_send_live_data",
    python_callable=fetch_and_send_crypto_data,
    dag=dag1,
)

t2 = PythonOperator(
    task_id="fetch_and_send_non_changing_data",
    python_callable=fetch_and_send_crypto_data,
    op_kwargs={"fetch_non_changing_data": True},
    dag=dag2,
)
