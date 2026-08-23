from __future__ import annotations

import pickle
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from ml.preprocessing import build_preprocessor, prepare_features
from ml.schema import TARGET_COLUMN

RANDOM_STATE = 42
TEST_SIZE = 0.2


def load_dataset(path: str | Path) -> tuple[pd.DataFrame, pd.Series]:
    dataset = pd.read_csv(path)

    if TARGET_COLUMN not in dataset.columns:
        raise ValueError(
            f"Missing target column: {TARGET_COLUMN}"
        )

    target = (dataset[TARGET_COLUMN] == "Not_Canceled").astype(int)

    features = dataset.drop(
        columns=[TARGET_COLUMN, "Booking_ID"],
        errors="ignore",
    )

    features = prepare_features(features)

    return features, target


def build_model() -> Pipeline:
    return Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            (
                "model",
                RandomForestClassifier(
                    n_estimators=300,
                    random_state=RANDOM_STATE,
                    n_jobs=-1,
                ),
            ),
        ]
    )


def train_model(
    dataset_path: str | Path,
) -> tuple[Pipeline, float]:
    features, target = load_dataset(dataset_path)

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=target,
    )

    pipeline = build_model()
    pipeline.fit(x_train, y_train)

    probabilities = pipeline.predict_proba(x_test)[:, 1]
    auc = roc_auc_score(y_test, probabilities)

    return pipeline, float(auc)


def save_artifact(
    pipeline: Pipeline,
    path: str | Path,
    metrics: dict[str, float],
) -> None:
    artifact = {
        "artifact_version": 1,
        "model_type": type(pipeline.named_steps["model"]).__name__,
        "pipeline": pipeline,
        "metrics": metrics,
        "random_state": RANDOM_STATE,
    }

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("wb") as handle:
        pickle.dump(artifact, handle)


def train_and_save(
    dataset_path: str | Path,
    artifact_path: str | Path,
) -> dict[str, float]:
    pipeline, auc = train_model(dataset_path)

    metrics = {
        "roc_auc": auc,
    }

    save_artifact(
        pipeline=pipeline,
        path=artifact_path,
        metrics=metrics,
    )

    return metrics
