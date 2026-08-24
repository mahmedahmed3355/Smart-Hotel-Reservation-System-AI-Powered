from pathlib import Path

DAG_PATH = (
    Path(__file__).resolve().parents[2]
    / "airflow_dags"
    / "model_retrain_dag.py"
)


def test_airflow_uses_package_email_agent_entrypoint() -> None:
    dag_source = DAG_PATH.read_text()

    assert "PYTHONPATH=backend python -m agents.email_agent" in dag_source
    assert "python agents/email_agent.py" not in dag_source
