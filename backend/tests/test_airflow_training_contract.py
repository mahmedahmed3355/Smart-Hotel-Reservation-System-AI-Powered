from pathlib import Path


def _dag_source() -> str:
    dag_path = Path(__file__).resolve().parents[2] / "airflow_dags" / "model_retrain_dag.py"
    return dag_path.read_text()


def test_airflow_uses_canonical_ml_training_cli():
    dag_source = _dag_source()

    assert "PYTHONPATH=backend python -m ml" in dag_source
    assert "--dataset" in dag_source
    assert "--output" in dag_source


def test_airflow_uses_configurable_dataset_and_model_paths():
    dag_source = _dag_source()

    assert "${DATA_CSV:-data/Hotel Reservations.csv}" in dag_source
    assert "${MODEL_PATH:-models/smart_hotel_model.pkl}" in dag_source


def test_airflow_does_not_use_legacy_training_path():
    dag_source = _dag_source()

    assert "ml/train_models.py" not in dag_source
