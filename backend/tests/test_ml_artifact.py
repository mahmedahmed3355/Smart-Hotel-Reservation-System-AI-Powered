import pickle
import sys
from pathlib import Path
from typing import ClassVar

import pytest

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1]),
)

import ml.artifact as artifact_module
from ml.artifact import ModelArtifactError, load_artifact


class ValidPipeline:
    named_steps: ClassVar[dict[str, object]] = {
        "preprocessor": object(),
        "model": object(),
    }

    def predict_proba(self, features):
        return [[0.1, 0.9]]


class PipelineWithoutPredictProba:
    named_steps: ClassVar[dict[str, object]] = {
        "preprocessor": object(),
        "model": object(),
    }


class PipelineWithoutNamedSteps:
    def predict_proba(self, features):
        return [[0.1, 0.9]]


class PipelineWithoutPreprocessor:
    named_steps: ClassVar[dict[str, object]] = {
        "model": object(),
    }

    def predict_proba(self, features):
        return [[0.1, 0.9]]


class PipelineWithoutModel:
    named_steps: ClassVar[dict[str, object]] = {
        "preprocessor": object(),
    }

    def predict_proba(self, features):
        return [[0.1, 0.9]]


def make_valid_artifact():
    return {
        "artifact_version": 1,
        "model_type": "RandomForestClassifier",
        "pipeline": ValidPipeline(),
        "metrics": {"roc_auc": 0.95},
        "random_state": 42,
    }


def write_artifact(path, artifact):
    with path.open("wb") as handle:
        pickle.dump(artifact, handle)


def test_resolve_model_path_uses_absolute_path(monkeypatch, tmp_path):
    absolute_path = tmp_path / "model.pkl"

    monkeypatch.setattr(
        artifact_module,
        "MODEL_PATH",
        str(absolute_path),
    )

    assert artifact_module.resolve_model_path() == absolute_path


def test_resolve_model_path_resolves_relative_to_backend(monkeypatch):
    monkeypatch.setattr(
        artifact_module,
        "MODEL_PATH",
        "models/test_model.pkl",
    )

    expected = (
        Path(artifact_module.__file__).resolve().parents[2]
        / "models/test_model.pkl"
    )

    assert artifact_module.resolve_model_path() == expected


def test_load_artifact_raises_when_file_is_missing(monkeypatch, tmp_path):
    missing_path = tmp_path / "missing.pkl"

    monkeypatch.setattr(
        artifact_module,
        "resolve_model_path",
        lambda: missing_path,
    )

    with pytest.raises(
        ModelArtifactError,
        match="Model artifact not found",
    ):
        load_artifact()


def test_load_artifact_returns_valid_artifact(monkeypatch, tmp_path):
    artifact_path = tmp_path / "model.pkl"
    expected = make_valid_artifact()

    write_artifact(
        artifact_path,
        expected,
    )

    monkeypatch.setattr(
        artifact_module,
        "resolve_model_path",
        lambda: artifact_path,
    )

    loaded = load_artifact()

    assert loaded["artifact_version"] == 1
    assert loaded["model_type"] == "RandomForestClassifier"
    assert loaded["metrics"] == {"roc_auc": 0.95}
    assert loaded["random_state"] == 42


def test_load_artifact_rejects_non_dictionary(monkeypatch, tmp_path):
    artifact_path = tmp_path / "model.pkl"

    write_artifact(
        artifact_path,
        ["not", "a", "dictionary"],
    )

    monkeypatch.setattr(
        artifact_module,
        "resolve_model_path",
        lambda: artifact_path,
    )

    with pytest.raises(
        ModelArtifactError,
        match="must be a dictionary",
    ):
        load_artifact()


def test_load_artifact_rejects_missing_required_keys(monkeypatch, tmp_path):
    artifact_path = tmp_path / "model.pkl"

    write_artifact(
        artifact_path,
        {
            "artifact_version": 1,
        },
    )

    monkeypatch.setattr(
        artifact_module,
        "resolve_model_path",
        lambda: artifact_path,
    )

    with pytest.raises(
        ModelArtifactError,
        match="missing keys",
    ):
        load_artifact()


def test_load_artifact_rejects_unsupported_version(monkeypatch, tmp_path):
    artifact_path = tmp_path / "model.pkl"
    invalid = make_valid_artifact()
    invalid["artifact_version"] = 2

    write_artifact(
        artifact_path,
        invalid,
    )

    monkeypatch.setattr(
        artifact_module,
        "resolve_model_path",
        lambda: artifact_path,
    )

    with pytest.raises(
        ModelArtifactError,
        match="Unsupported artifact version",
    ):
        load_artifact()


def test_load_artifact_rejects_pipeline_without_predict_proba(
    monkeypatch,
    tmp_path,
):
    artifact_path = tmp_path / "model.pkl"
    invalid = make_valid_artifact()
    invalid["pipeline"] = PipelineWithoutPredictProba()

    write_artifact(
        artifact_path,
        invalid,
    )

    monkeypatch.setattr(
        artifact_module,
        "resolve_model_path",
        lambda: artifact_path,
    )

    with pytest.raises(
        ModelArtifactError,
        match="predict_proba",
    ):
        load_artifact()


def test_load_artifact_rejects_pipeline_without_named_steps(
    monkeypatch,
    tmp_path,
):
    artifact_path = tmp_path / "model.pkl"
    invalid = make_valid_artifact()
    invalid["pipeline"] = PipelineWithoutNamedSteps()

    write_artifact(
        artifact_path,
        invalid,
    )

    monkeypatch.setattr(
        artifact_module,
        "resolve_model_path",
        lambda: artifact_path,
    )

    with pytest.raises(
        ModelArtifactError,
        match="valid sklearn pipeline",
    ):
        load_artifact()


def test_load_artifact_rejects_missing_preprocessor(
    monkeypatch,
    tmp_path,
):
    artifact_path = tmp_path / "model.pkl"
    invalid = make_valid_artifact()
    invalid["pipeline"] = PipelineWithoutPreprocessor()

    write_artifact(
        artifact_path,
        invalid,
    )

    monkeypatch.setattr(
        artifact_module,
        "resolve_model_path",
        lambda: artifact_path,
    )

    with pytest.raises(
        ModelArtifactError,
        match="missing the preprocessor",
    ):
        load_artifact()


def test_load_artifact_rejects_missing_model_step(
    monkeypatch,
    tmp_path,
):
    artifact_path = tmp_path / "model.pkl"
    invalid = make_valid_artifact()
    invalid["pipeline"] = PipelineWithoutModel()

    write_artifact(
        artifact_path,
        invalid,
    )

    monkeypatch.setattr(
        artifact_module,
        "resolve_model_path",
        lambda: artifact_path,
    )

    with pytest.raises(
        ModelArtifactError,
        match="missing the model step",
    ):
        load_artifact()
