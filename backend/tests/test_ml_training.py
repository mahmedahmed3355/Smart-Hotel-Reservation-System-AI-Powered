import pandas as pd
import pytest
from sklearn.pipeline import Pipeline

from ml.training import (
    build_model,
    load_dataset,
    save_artifact,
    train_and_save,
    train_model,
)


def test_load_dataset_contract():
    features, target = load_dataset(
        "data/Hotel Reservations.csv"
    )

    assert features.shape == (36275, 17)
    assert target.shape == (36275,)
    assert sorted(target.unique().tolist()) == [0, 1]


def test_load_dataset_requires_target(tmp_path):
    dataset = pd.DataFrame(
        [
            {
                "no_of_adults": 2,
                "Booking_ID": "H1",
            }
        ]
    )

    path = tmp_path / "invalid.csv"
    dataset.to_csv(path, index=False)

    with pytest.raises(
        ValueError,
        match="Missing target column",
    ):
        load_dataset(path)


def test_build_model_returns_pipeline():
    pipeline = build_model()

    assert isinstance(pipeline, Pipeline)
    assert list(pipeline.named_steps.keys()) == [
        "preprocessor",
        "model",
    ]
    assert pipeline.named_steps["model"].n_estimators == 300
    assert pipeline.named_steps["model"].random_state == 42


def test_train_model_returns_auc_and_pipeline():
    pipeline, auc = train_model(
        "data/Hotel Reservations.csv"
    )

    assert isinstance(pipeline, Pipeline)
    assert isinstance(auc, float)
    assert 0.90 <= auc <= 1.0
    assert "preprocessor" in pipeline.named_steps
    assert "model" in pipeline.named_steps


def test_save_artifact_round_trip(tmp_path):
    pipeline = build_model()

    artifact_path = tmp_path / "model.pkl"

    save_artifact(
        pipeline=pipeline,
        path=artifact_path,
        metrics={"roc_auc": 0.95},
    )

    assert artifact_path.exists()

    import pickle

    with artifact_path.open("rb") as handle:
        artifact = pickle.load(handle)

    assert artifact["artifact_version"] == 1
    assert artifact["model_type"] == "RandomForestClassifier"
    assert artifact["metrics"] == {"roc_auc": 0.95}
    assert artifact["random_state"] == 42
    assert "preprocessor" in artifact["pipeline"].named_steps
    assert "model" in artifact["pipeline"].named_steps


def test_train_and_save_creates_valid_artifact(tmp_path):
    artifact_path = tmp_path / "smart_hotel_model.pkl"

    metrics = train_and_save(
        dataset_path="data/Hotel Reservations.csv",
        artifact_path=artifact_path,
    )

    assert artifact_path.exists()
    assert "roc_auc" in metrics
    assert 0.90 <= metrics["roc_auc"] <= 1.0
