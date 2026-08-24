from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {"owner":"hotel", "retries":1, "retry_delay": timedelta(minutes=5)}

with DAG(
    dag_id="hotel_pipeline",
    start_date=datetime(2025,1,1),
    schedule_interval="0 3 * * *",  # يومياً 3 صباحاً
    catchup=False,
    default_args=default_args,
) as dag:

    retrain = BashOperator(
        task_id="retrain_models",
        bash_command=(
            "cd /opt/airflow/repo && . venv/bin/activate && "
            "PYTHONPATH=backend python -m ml "
            "--dataset \"${DATA_CSV:-data/Hotel Reservations.csv}\" "
            "--output \"${MODEL_PATH:-models/smart_hotel_model.pkl}\""
        )
    )

    run_email_agent = BashOperator(
        task_id="run_email_agent",
        bash_command=(
            "cd /opt/airflow/repo && . venv/bin/activate && "
            "PYTHONPATH=backend python -m agents.email_agent"
        )
    )

    retrain >> run_email_agent
