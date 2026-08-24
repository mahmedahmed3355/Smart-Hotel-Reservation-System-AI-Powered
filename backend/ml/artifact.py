from __future__ import annotations

import pickle
from pathlib import Path

from config.settings import MODEL_PATH


class ModelArtifactError(RuntimeError):
    pass


def resolve_model_path() -> Path:
    configured = Path(MODEL_PATH or "models/smart_hotel_model.pkl")

    if configured.is_absolute():
        path = configured
    else:
        project_root = Path(__file__).resolve().parents[2]
        path = project_root / configured

    return path


def load_artifact() -> dict:
    path = resolve_model_path()

    if not path.exists():
        raise ModelArtifactError(
            f"Model artifact not found: {path}. "
            "Run the training pipeline first."
        )

    try:
        with path.open("rb") as handle:
            artifact = pickle.load(handle)
    except (OSError, pickle.PickleError, EOFError, ValueError) as exc:
        raise ModelArtifactError(
            f"Failed to load model artifact: {path}"
        ) from exc

    if not isinstance(artifact, dict):
        raise ModelArtifactError("Model artifact must be a dictionary.")

    required_keys = {
        "artifact_version",
        "model_type",
        "pipeline",
        "metrics",
        "random_state",
    }

    missing = required_keys - artifact.keys()

    if missing:
        raise ModelArtifactError(
            f"Model artifact is missing keys: {sorted(missing)}"
        )

    if artifact["artifact_version"] != 1:
        raise ModelArtifactError(
            f"Unsupported artifact version: {artifact["artifact_version"]}"
        )

    pipeline = artifact["pipeline"]

    if not hasattr(pipeline, "predict_proba"):
        raise ModelArtifactError(
            "Model artifact pipeline does not support predict_proba()."
        )

    if not hasattr(pipeline, "named_steps"):
        raise ModelArtifactError(
            "Model artifact does not contain a valid sklearn pipeline."
        )

    if "preprocessor" not in pipeline.named_steps:
        raise ModelArtifactError(
            "Model pipeline is missing the preprocessor step."
        )

    if "model" not in pipeline.named_steps:
        raise ModelArtifactError(
            "Model pipeline is missing the model step."
        )

    return artifact
